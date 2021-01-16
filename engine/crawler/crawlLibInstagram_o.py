import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import unicodedata
import os
import pymysql
from sqlalchemy import create_engine
import pickle
from engine.sql.almaden import Sql


class CrawlLibInstagram:

        def __init__(self,task_id=None,keyword=None,num_content=None):

            self.user = 'gimseungo546'
            self.password = 'almaden7025!'
            self.task_id = task_id
            self.keyword = keyword.replace(" ","")

            self.num_content = num_content
            self.driver = self.set_selenium()
            self.db = Sql('datacast2')
        def __del__(self):
            try:
                self.driver.close()
            except:
                pass

        def get_keyword_content_num(self, keyword):

            url_tag = 'https://www.instagram.com/explore/tags/%s' % (keyword)

            self.driver.get(url_tag)
            WebDriverWait(self.driver, 2).until(
                visibility_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span')))

            content_num = self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').text
            return content_num

        def crawl_total(self):
            ###user 정보 셋팅
            user = self.user
            password = self.password
            content_num = 0
            try:
                ##login
                self.login(user, password,keyword=self.keyword)
            except Exception as e:
                self.driver.close()
                print(e, 'insta_login_error')

            ##search_keyword 에 대한 게시글 수 가져오기
            try:
                keyword = self.keyword
                content_num = self.get_keyword_content_num(keyword)
            except Exception as e:
                self.driver.close()
                print(e, 'insta_login_error')
            content_num = str(content_num)
            content_num = int(content_num.replace(',',''))
            self.db.update_one('crawl_task','n_total',content_num,'task_id',self.task_id)

        def cleanser(self,text):
            text = re.sub(u"(http[^ ]*)", " ",text)
            text = re.sub(u"@(.)*\s", " ", text)
            text = re.sub(u"#", "", text)
            text = re.sub(u"\\d+", " ", text)
            text = re.sub(u"\\s+", " ",text)
            return text

        def get_stop_keyword(self):
            stop_tag = ["#인스타그램", "#인스타", "#팔로우", "#맞팔", "#인친", "#셀스타그램", "#그램", "#스타","#행복","#일상","#오늘","#소통","#좋반"]
            return stop_tag

        def gethtmltext(self,soup):
            htmltext_list = []
            try:
                # print(soup)
                # input()
                htmltext = re.findall(r'\"edge_media_to_caption\":{\"edges\":\[[^]}]+',soup.text)
                # print(htmltext)
                htmltext = htmltext[0].split('"edge_media_to_caption":{"edges":[{"node":')[1]
                htmltext = htmltext+"}"
                htmltext = json.loads(htmltext,encoding='utf-8')
                htmltext = htmltext['text']
                htmltext = htmltext.replace('\n','')
                htmltext = self.cleanser(htmltext)
                htmltext = unicodedata.normalize('NFC', htmltext)

            except Exception as e:
                print('htmltext error',e)
                htmltext = ''

            htmltext_list.append(htmltext)
            return htmltext

        def getreply(self,soup):
            # # 정규표현식 content 변수의 본문 내용중  # 으로 시작하며, #뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우)를 모두 찾아 tags 변수에 저장
            reply_body = ''

            try:
                js_list = soup.find_all('script', {'type': "text/javascript"})
            except Exception as e:
                reply_body = ''
                return reply_body

            for index, js in enumerate(js_list):

                try:
                    reply_js = str(js)
                    reply_text = reply_js.split('edge_media_to_parent_comment')[1]
                    index_first = reply_text.find("{")
                    index_last = reply_text.rfind("}")
                    reply_text = reply_text[index_first:index_last + 1]

                    reply_text = reply_text.split(',"edge_media_to_hoisted_comment"')[0]
                    reply_to_json = json.loads(reply_text)
                    edges = reply_to_json['edges']
                    for edge in edges:
                        reply_body += edge['node']['text']
                        reply_body = unicodedata.normalize('NFC', reply_body)

                except Exception as e:
                    continue
            return reply_body

        def getloc(self,soup):
            try:
                ##location 추출하기
                locations = re.findall(r'\"location\":[^}]+',soup.text)
                location = locations[0].split(',"address_json"')[0]
                location = location.split('\"location\":')[1]
                location_json_style= location+'}'
                location_to_json = json.loads(location_json_style)
                location = location_to_json['name']
            except Exception as e:
                location = ''

            return location


        def gethashtag(self,soup):
            stop_tag = self.get_stop_keyword()
            total_tag = ''
            try:

                ##hashtag 만 추출하기
                tags = re.findall(r'#[^\s#,\\}\]\"]+', soup.text)
                for tag in tags:
                    if tag not in stop_tag:
                        tag = re.sub(u"(http[^ ]*)", " ", tag)
                        tag = re.sub(u"@(.)*\s", " ", tag)
                        tag = re.sub(u"\\s+", " ", tag)
                        tag = unicodedata.normalize('NFC',tag)
                        total_tag += tag

            except Exception as e:
                pass
            return total_tag

        def set_selenium(self):
            chrome_options = Options()
            # self.PROXY = "{}:{}@{}:{}".format('khopaE','CHXfnA','45.158.186.10','16902')  # IP:PORT or HOST:PORT
            self.PROXY = "{}:{}@{}:{}".format('s772hc', 'p62Fpp', '185.80.149.218', '8000')  # IP:PORT or HOST:PORT
            PROXY  =self.PROXY
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36")
            chrome_options.add_argument("lang=ko_KR")  # 한국어!
            # chrome_options.add_argument("--headless")
            # chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("disable-dev-shm-usage")
            # chrome_options.add_argument('--disable-gpu')
            # webdriver.DesiredCapabilities.CHROME['proxy'] = {
            #     'httpProxy': PROXY,
            #     'ftpProxy' : PROXY,
            #     'sslProxy': PROXY,
            #     "proxyType" : "MANUAL"
            # }
            driver = webdriver.Chrome(options=chrome_options,
                                      executable_path='chromedriver.exe')
            return driver

        def login(self,user,password,keyword):
            user = user
            password = password
            keyword = keyword

            url = 'https://www.instagram.com/explore/'
            self.driver.get(url)
            self.driver.implicitly_wait(10)


            ##쿠키 정보 저장
            file_list = os.listdir("./")
            if "cookies.pkl" not in file_list:
                pickle.dump(self.driver.get_cookies(),open("cookies.pkl","wb"))
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            ##id, pw 입력
            WebDriverWait(self.driver, 10).until(visibility_of_element_located((By.CSS_SELECTOR, 'button.sqdOP.L3NKy.y3zKF')))
            login_id = self.driver.find_element_by_css_selector('input[name="username"]')
            login_id.send_keys(user)
            login_pw = self.driver.find_element_by_css_selector('input[name="password"]')
            login_pw.send_keys(password)
            self.driver.implicitly_wait(10)

            ##login 시도
            login_button = self.driver.find_element_by_css_selector('button.sqdOP.L3NKy.y3zKF')
            login_button.click()
            self.driver.implicitly_wait(3)

            ##로그인 정보 저장 설정
            WebDriverWait(self.driver, 1000).until(
                visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div/div/div/button')))
            login_info_save_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
            login_info_save_button.click()
            self.driver.implicitly_wait(10)
            ####

            # url_tag = 'https://www.instagram.com/explore/tags/%s' % (keyword)
            #
            # self.driver.get(url_tag)

        def get_url(self,num_content):
            num_content = num_content
            #
            # total_content_num = driver.find_element_by_xpath(
            #     "/html/body/div[1]/section/main/header/div[2]/div[1]/div[2]/span/span")
            # total_content_num = total_content_num.text
            # total_content_num = total_content_num.replace(",", "")
            # total_content_num = int(total_content_num)

            break_cnt = 0
            total_post_url = []
            unique_total_post_url = []
            while True:

                last_height = self.driver.execute_script("return document.body.scrollHeight")

                ##현재 스크롤 상태에서 존재하는 게시글을 가져온다.(최근게시글)
                posts = self.driver.find_elements_by_css_selector('.v1Nh3 a')
                for post in posts:
                    post_url = post.get_attribute('href')
                    print(post_url)
                    total_post_url.append(post_url)

                    ##중복제거
                    [unique_total_post_url.append(post_url) for url in total_post_url if url not in unique_total_post_url]

                unique_total_post_url = unique_total_post_url[0:num_content]

                ##게시글이 더 없을경우 빠져나간다.
                ##만약 전체 게시글 수가 클라이언트가 요구하는 수보다 작으면 스크롤을 내리고 while 처음으로 돌아간다.
                if len(unique_total_post_url) < num_content:

                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.driver.implicitly_wait(20)
                    time.sleep(0.5)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break_cnt += 1
                        print("{}={}".format(new_height, last_height))

                        if break_cnt >= 20:
                            break

                    elif new_height != last_height:
                        break_cnt = 0

                    continue
                ##필요한 게시물만큼 가져왔으면 반복문을 빠져나간다.

                elif len(unique_total_post_url) >= num_content:
                    break
                ##더이상 게시물이 없는 경우 반복문을 빠져나간다.

            ##url 읽어서 본문 내용 가져오기
            return unique_total_post_url

        def seleniumCookieToRequest(self):
            self.driver.get_cookies()
            sess = requests.session()
            sess.proxies = {
                "http":"http://{}".format(self.PROXY),
                "https":"https://{}".format(self.PROXY)
            }
            sess.headers.update({'user-agent': "headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}"})
            sess.cookies.update({c['name']: c['value'] for c in self.driver.get_cookies()})
            return sess

        def get_url_main(self):

            user = self.user
            password = self.password
            keyword = self.keyword
            num_content = self.num_content

            ##드라이버 세팅

            ##로그인
            try:
                self.login(user,password,keyword)
            except Exception as e:
                self.driver.close()
                print(e, 'insta_login_error')
                return 0,0
            ##urllist 가져오기
            urllist = self.get_url(num_content)
            ##드라이버 쿠키 request 에 전달
            sess = self.seleniumCookieToRequest()
            self.driver.close()
            return sess,urllist

        def get_body_main(self,sess,urllist):

            ##ruequest로 soup 가져오기
            content_list = []
            for index, url in enumerate(urllist):
                # if index%10==0:

                try:
                    print(self.keyword,index,url)
                    with sess as s:
                        time.sleep(0.5)
                        res = s.get(url,headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'})
                        print(res.status_code)
                        html = res.text
                        soup = BeautifulSoup(html, "lxml")

                except Exception as e:
                    print(e)
                    continue

                keyword = self.keyword
                htmltext = self.gethtmltext(soup)
                reply = self.getreply(soup)
                location = self.getloc(soup)
                hashtag = self.gethashtag(soup)
                task_id = self.task_id
                content_dict = {'task_id':task_id,'text': htmltext,'keyword':keyword ,'reply':reply, 'location':location, 'hashtag':hashtag, 'channel': 'instagram'}
                print('content_dict:',content_dict)
                content_list.append(content_dict)

            insta_dataframe =pd.DataFrame(content_list, columns=['task_id','keyword','text','reply','location','hashtag','channel'])
            insta_dataframe.to_excel('insta_{}_{}.xlsx'.format(self.keyword,self.num_content),engine='xlsxwriter')

            engine = create_engine(
                ("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4").format('root',
                                                                       'robot369',
                                                                       '1.221.75.76',
                                                                       3306,
                                                                       'datacast2'))
            insta_dataframe.to_sql(name='cdata', con=engine, if_exists='append', index=False)

        def crawinstagram(self):
            sess,urllist = self.get_url_main()
            print('get_url_main 완료')
            if (sess,urllist) == (0,0):
                print('error')
                return 0
            else:
                try:
                    conn = pymysql.connect(host='1.221.75.76',
                                           port=3306, user='root', password='robot369',
                                           db='datacast2',
                                           charset='utf8mb4')
                    sql_insert_task = "insert into task_log (keyword,channel,nCrawl,nCrawled,comment) " \
                                      "values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (
                                          self.keyword, 'instagram', self.num_content, len(urllist), 'instagram'
                                      )
                    print(sql_insert_task)

                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs.execute(sql_insert_task)
                    self.task_id = curs.lastrowid
                    conn.commit()
                    print('to get body')
                    conn.close()
                    self.get_body_main(sess,urllist)
                except Exception as e:
                    print(e)
                    return
# splitting the string based on , we get key value pairs


