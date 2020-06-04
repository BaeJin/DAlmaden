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
from collections import Counter
from konlpy.tag import Okt
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from konlpy.tag import Twitter
from MeCab import Tagger as Mecab
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

class SqlPandas :
    def __init__(self, dbName,
                 hostIP='106.246.169.202', userID='root', password='robot369', charset='utf8mb4'):
        sqlEngine = create_engine('mysql')

class Sql :
    def __init__(self, dbName, comment = "",
                 hostIP='106.246.169.202', userID='root', password='robot369', charset='utf8mb4'):
        self.dbName = dbName
        self.hostIP = hostIP
        self.userID = userID
        self.password = password
        self.charset = charset
        self.conn = None
        self.curs = None
        self.connect()

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
        select_where = " and ".join([k+"="+v for k, v in params.items()])
        count = self.select(tablename, where=select_where, count=True)
        if count>0 : return True
        else : return False

    def insert_withoutDuplication(self, tablename, check_list, **params):
        new_params = {}
        for k,v in params.items() :
            if k in check_list :
               new_params[k] = v
        if self.check_duplication(tablename, **new_params) :
            return None
        else :
            return self.insert(tablename, **params)

    def insert(self, tablename, **params):
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





class Nlp :
    def __init__(self, nlpEngine = "Mecab"):
        '''
        원하는 형태소 분석기 엔진으로 형태소 분석기 생성
        :param nlpEngine: 형태소 분석기 이름(첫글자 대문자) str
        '''
        self.nlpEngine = nlpEngine
        if nlpEngine == "Okt":
            self.nlp = Okt()
        elif nlpEngine == "Komoran":
            self.nlp = Komoran()
        elif nlpEngine == "Kkma":
            self.nlp = Kkma()
        elif nlpEngine == "Hannanum":
            self.nlp = Hannanum()
        elif nlpEngine == "Mecab":
            self.nlp = Mecab()
        elif nlpEngine == "Twitter":
            self.nlp = Twitter()
        else:
            raise NameError("unknown nlp name")

    def cleanse_korean(self, sentence, remove_words=['span','class','quot','br']):
        rt = sentence
        for remove_word in remove_words :
            rt = re.sub(remove_word, "", rt)
        rt = re.sub(u"(http[^ ]*)", " ", rt)
        rt = re.sub(u"@(.)*\s", " ", rt)
        rt = re.sub(u"#", "", rt)
        rt = re.sub(u"\\d+", " ", rt)
        rt = re.sub(u"[^가-힣A-Za-z]", " ", rt)
        rt = re.sub(u"\\s+", " ", rt)

        return rt


    def tokenize(self, sentence, norm=True, stem=True, join=False):
        if self.nlpEngine == "Mecab":
            try :
                a = self.nlp.parse(sentence)
                b = [aa.split(',') for aa in a.split('\n')][:-2]
                if stem :
                    s = [[d[3],d[0].split('\t')[1]] for d in b]
                else :
                    s = [d[0].split('\t') for d in b]
                if join :
                    j = ['/'.join(ss) for ss in s]
                else :
                    j = [tuple(ss) for ss in s]
                return j
            except :
                return []
        else :
            return self.nlp.pos(sentence, norm=norm, stem=stem, join=join)

    def get_nounList(self, phrase) :
        '''
        문장으로부터 명사 리스트 추출
        :param phrase: 문장 str
        :return: 명사로 이루어진 리스트 list of str
        '''
        if self.nlpEngine == "Mecab" :
            all_tags_raw1 = self.nlp.parse(phrase).split("\n")
            all_tags_raw2 = [tt.split(",")[0] for tt in all_tags_raw1]
            all_tags = [t.split("\t") for t in all_tags_raw2]
            nounList = []
            for tags in all_tags :
                if len(tags) == 2 :
                    if tags[1][0:2] in ['NN','NP'] :
                        nounList.append(tags[0])
            print(nounList)
            return nounList
        else :
            return self.nlp.nouns(phrase)

    def get_nounLists(self, phrase_list) :
        '''
        문장 리스트로부터 명사 리스트의 리스트 추출
        len(phrase_list) == len(nounLists)
        :param phrase_list: 문장 리스트 list of str
        :return: 명사 리스트의 리스트 list of list of str
        '''
        nounLists = []
        for i, phrase in enumerate(phrase_list) :
            if i % 100 == 0:
                print(i)
            nounLists.append(self.get_nounList(phrase))
        return nounLists

    def get_nounCount(self, phrase):
        '''
        문장으로부터 명사 빈도 추출
        :param phrase: 문장 str
        :return: 명사 빈도 {명사:빈도,...} dict
        '''
        return dict(Counter(self.get_nounList(phrase)).most_common())

    def get_nounCounts(self, phrase_list):
        '''
        문장 리스트로부터 명사 빈도 딕셔너리의 리스트 추출
        len(phrase_list) == len(nounCounts)
        :param phrase_list: 문장 리스트 list of str
        :return: 명사 빈도 리스트[{명사:빈도,...},{명사:빈도,...}] list of dict
        '''
        nounCounts = []
        for i, phrase in enumerate(phrase_list):
            if i%100 == 0 :
                print(i)
            nounCounts.append(self.get_nounCount(phrase))
        return nounCounts

    def get_nounList_by_list(self, phrase_list):
        '''
        문장 리스트로부터 명사 리스트 추출
        :param phrase_list: 문장 리스트 list of str
        :return: 명사 리스트 list of str
        '''
        nounLists = self.get_nounLists(phrase_list)
        nounList = []
        for l in nounLists :
            nounList.extend(l)
        return nounList

    def get_nounCount_by_list(self, phrase_list):
        '''
        문장 리스트로부터 명사 빈도 추출
        :param phrase_list: 문장 리스트 list of str
        :return: 명사 빈도{명사:빈도,...} dict
        '''
        nounList = self.get_nounList_by_list(phrase_list)
        return dict(Counter(nounList).most_common())

class File :
    def __init__(self, dir):
        self.dir = dir


