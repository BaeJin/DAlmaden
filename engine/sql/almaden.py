from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymysql
import os
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
import datetime
import pandas as pd

def cleanse(text) :
    #DB 저장을 위한 최소한의 클린징
    text = re.sub(u"[^\x20-\x7E가-힣]"," ",text)
    text = re.sub(u"\\s+", " ", text)
    return text.strip()

class SeleniumDriver :
    def __init__(self):
        '''
        Almaden SeleniumCrawler 1.0
        date 2020-02-18
        by Bae Jin
        '''
        #option
        self.option = Options()
        self.option.add_argument("--disable-infobars")
        self.option.add_argument("start-maximized")
        self.option.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        self.option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        path = os.path.dirname(os.path.realpath(__file__))
        self.driver = webdriver.Chrome(options=self.option, executable_path=path + "\webdrivers\chromedriver.exe")
        self.wait = None

    def get(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def find_elements_by_xpath(self,xpath):
        return self.driver.find_elements_by_xpath(xpath)
    def find_element_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def scrollDown(self, scnum=1, wait=0.1, interval=1):
        print("scroll down!")
        scrollnum = 0
        while scrollnum <= scnum:
            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            print(last_height)
            #print("\n\n\nScroll_Down**************\n\n\n")
            for i in range(0,last_height*0.5,int(last_height*0.5/interval)) :
                if i == 0 : continue
                print(i)
                self.driver.execute_script("window.scrollBy(0, %d)"%(i))
                time.sleep(wait)
            self.driver.execute_script("window.scrollTo(0,%d)" % (last_height))
            self.driver.implicitly_wait(3)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            scrollnum += 1

    def waitUntil_className(self, className, sec=1000):
        WebDriverWait(self.driver, sec).until(EC.element_to_be_clickable((By.CLASS_NAME, className)))
        # try:
        #     element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "change-theme")))
        #     driver.implicitly_wait(3)
        #     # c_elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]")
        #     # c_elem.click()
        #     time.sleep(5)
        # finally:
        #     print("phase 2")

class Sql :
    def __init__(self, dbName, comment = "",
                 hostIP='1.221.75.76',
                 userID='root', password='robot369', charset='utf8mb4'):
        self.dbName = dbName
        self.hostIP = hostIP
        self.userID = userID
        self.password = password
        self.charset = charset
        self.conn = None
        self.curs = None
        self.connect()
        self.sql_alchemy_engine = create_engine(
            ("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8").format
                               (userID,
                                password,
                                hostIP,
                                3306,
                                dbName),
                                encoding='utf-8')

    def connect(self):
        self.conn = pymysql.connect(host=self.hostIP, user=self.userID, password=self.password,
                               db=self.dbName, charset=self.charset)
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    def query(self, query):
        self.curs.execute(query)
        self.conn.commit()
    def close(self):
        self.conn.close()

    def update_one(self,tableName, field, value, field_id, id):
        if type(value) is str :
            value = '"'+value+'"'
        query = '''update {tableName} set {field} = {value} where {field_id}={id}'''.format(
            tableName = tableName,
            field = field,
            value=value,
            field_id = field_id,
            id=id
        )
        self.query(query)

    def select(self, tablename, what="", where="", asDataFrame=False, count=False):
        '''
        e.g. select('tablename', 'id, keyword, title', 'date like "2019%"', True)
        :param tablename: table name
        :param params: field = value or // field like %value%
        :param count:
        :return:
        '''
        if count :
            select_what = "count(*)"
        else :
            if len(what)<1 :
                select_what = "*"
            else :
                select_what = what
        sql = "select %s from %s"%(select_what, tablename)
        if len(where) > 1:
            sql+=" where "+where

        self.curs.execute(sql)
        rows = self.curs.fetchall()
        if count :
            return int(rows[0]['count(*)'])
        else :
            if asDataFrame :
                return pd.DataFrame(rows)
            else :
                return rows

    def check_duplication(self, tablename, **params):
        select_where = " and ".join([k+"="+"'{}'".format(v) if type(v)==str else k+"="+str(v) for k, v in params.items()])
        count = self.select(tablename, where=select_where, count=True)
        if count>0 : return True
        else : return False

    def insert_withoutDuplication(self, tablename, check_list, **params):
        '''
        e.g. insert_withoutDuplication('datatable', ['keyword','url'], keyword = 'abc', url = 'http://', date = '20150305', title = '테스트')
        :param tablename: str
        :param check_list: list
        :param params: dict
        :return: None or id(int)
        '''
        new_params = {}
        for k,v in params.items() :
            if k in check_list :
               new_params[k] = v
        if self.check_duplication(tablename, **new_params) :
            return None
        else:
            return self.insert(tablename, **params)

    def update_multi(self,tablename,update_dict:dict, where_dict:dict):

        update_sql = "update %s set "%(tablename) + ",".join([key+"="+"%s" for key in update_dict.keys()])
        where_sql = "where " + "and".join([key+"="+"%s" for key in where_dict.keys()])
        sql = update_sql +' '+where_sql
        update_set_value = list(update_dict.values())
        where_value = list(where_dict.values())
        value = update_set_value + where_value
        self.curs.execute(sql,value)
        self.conn.commit()

    def insert(self, tablename, **params):
        '''
        e.g. insert('datatable', date = '20150305', title = '테스트')
        :param tablename: str
        :param params: dict
        :return: id(int)
        '''
        len_params = len(params)
        sql = "insert into %s("%(tablename)
        for k in params.keys() :
            sql += str(k)+","
        sql = sql[:-1]+") values("
        for i in range(len_params) :
            sql += "%s"+","
        sql = sql[:-1]+")"
        v = tuple(params.values())
        self.curs.execute(sql, v)
        row_id = self.curs.lastrowid
        self.conn.commit()
        return row_id


    def get_now_datetime(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

