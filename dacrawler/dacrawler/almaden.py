import pymysql
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymysql
import os
import random
import colorsys
import time
import re
import math
import operator
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

import pandas as pd

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

class Sql:
    def __init__(self, dbName, hostIP, port, userID, password, charset='utf8mb4'):
        self.__dbName = dbName
        self.__port = port
        self.__hostIP = hostIP
        self.__userID = userID
        self.__password = password
        self.__charset = charset
        self.__conn = None
        self.__curs = None
        self.__connect()

    def __connect(self):
        self.__conn = pymysql.connect(host=self.__hostIP, port=self.__port, user=self.__userID,
                                      password=self.__password,
                                      db=self.__dbName, charset=self.__charset)
        self.__curs = self.__conn.cursor(pymysql.cursors.DictCursor)

    def __close(self):
        self.__conn.close()


    def select(self, tablename, what="", where="", asDataFrame=False):
        select_what = "*" if len(what) < 1 else what
        sql = "select %s from %s" % (select_what, tablename)
        sql = sql + " where " + where if len(where) > 1 else sql
        self.__curs.execute(sql)
        rows = self.__curs.fetchall()
        return pd.DataFrame(rows) if asDataFrame else rows

    def count(self, tablename, where=""):
        sql = "select count(*) from %s" % (tablename)
        sql = sql + " where " + where if len(where) > 1 else sql
        print('finish_sql:',sql)
        self.__curs.execute(sql)
        rows = self.__curs.fetchall()
        count = int(rows[0]['count(*)'])
        return count

    def update(self, tableName, rowId, colname_id='id', **params):
        if len(params) < 1: return
        set_query = '=%s,'.join(params.keys()) + '=%s'
        query = f'update {tableName} set {set_query} where {colname_id}={rowId}'
        values = self._get_executeValues(params.values())
        self.__curs.execute(query, values)
        self.__conn.commit()

    def delete(self, tableName, rowId, colname_id='id'):
        query = f'delete from {tableName} where {colname_id}={rowId}'
        self.__curs.execute(query)
        self.__conn.commit()

    def insert(self, tablename, **params):
        # e.g. insert('datatable', date = '20150305', title = '테스트')

        sql = "insert into %s(" % (tablename) + ",".join([str(k) for k in params.keys()]) + ") values(" + \
              ",".join(["%s"] * len(params)) + ")"
        print(sql)
        vs = self._get_executeValues(params.values())
        self.__curs.execute(sql, vs)
        row_id = self.__curs.lastrowid
        self.__conn.commit()
        return row_id

    def insert_withoutDuplication(self, tablename, check_list, **params):
        '''
        e.g. insert_withoutDuplication('datatable', ['keyword','url'],    keyword = 'abc', url = 'http://', date = '20150305', title = '테스트')
        '''
        new_params = {}
        for k, v in params.items():
            if k in check_list:
                new_params[k] = v
        if self.check_duplication(tablename, **new_params):
            print('duplicated')
            return None
        else:
            return self.insert(tablename, **params)

    def check_duplication(self, tablename, **params):
        select_where = " and ".join([k + "= '"+v+"'" for k, v in params.items()])
        print('select_where:',select_where)
        count = self.count(tablename, where=select_where)
        if count > 0:
            return True
        else:
            return False

    def _get_executeValues(self, inputValues):
        executeValues = [v if (type(v) is int or type(v) is float) else str(v) if v else None for v in inputValues]
        executeValues = tuple(executeValues)
        return executeValues