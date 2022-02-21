from pathlib import Path
import sys
from naver_cafe.setting import settings
from engine.sql.almaden import Sql
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import requests
from datetime import datetime
import pandas as pd
import pickle
from contextlib import suppress
import re
from html import unescape
db = Sql("datacast2")

class CrawlLibNaverCafe:
    def __init__(self,keyword):
        self.keyword = keyword

    def get_driver(self):
        ### 크롬 드라이버 실행
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--dns-prefetch-disable")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self):
        self.driver.find_element(By.XPATH, '//*[@id="gnb_login_button"]').click()
        self.driver.find_element(By.XPATH, '//*[@id="id"]').send_keys(self.username)
        self.driver.find_element(By.XPATH, '//*[@id="pw"]').send_keys(self.password)
        self.driver.find_element(By.XPATH, '//*[@id="log.login"]').click()

    def get_setting_info(self):
        setting_info = None
        try:
            setting_info = list(filter(lambda x : self.keyword in x.keys(),settings.info_list))[0][self.keyword]
        except Exception:
            print("task keyword 가 잘못되었습니다.")
        return setting_info

    def select_task_id(self):
        row = db.select("crawl_task",'task_id','keyword=\"%s\" and channel=\"%s\"'%(self.keyword,"navercafe"))
        if len(row)>0:
            task_id = row[0]["task_id"]
        else:
            raise ValueError("task_id 에 해당하는 값이 없습니다.")
        return task_id

    def setting(self):
        # setting
        setting_info = self.get_setting_info()
        self.task_id = self.select_task_id()
        self.username = setting_info["username"]
        self.password = setting_info["password"]
        self.page_link = setting_info["link"]
        self.login_required = setting_info["login_required"]

    def crawl_urllist(self):
        self.setting()
        self.get_driver()
        self.driver.get(url=self.page_link)
        ### 키워드 수집 정보
        num_per_page = 15  # 페이지당 게시글 갯수(default: 15개)
        address_list = []
        page = 1

        l = True
        while l:
            time.sleep(0.5)
            ### 현재 페이지의 html 불러오기
            r = None
            try:
                r = self.driver.page_source
            except TimeoutException as ex:
                print('TimeoutException', ex)
                self.driver.get(url=self.page_link)
                r = self.driver.page_source

            page_html = BeautifulSoup(r, "html.parser")
            #         로그인 안한 경우 아래로 진행

            content = page_html.find_all("div", class_="article-board m-tcol-c")[1].find('tbody')
            if content == None:
                content = page_html.find("div", class_="article-board result-board m-tcol-c").find('tbody')
            body = content.find_all("tr")
            ### 게시글 정보 저장하기
            for x in body:
                temp_dict = {}
                if x.find("div", class_="board-list") is not None:
                    # <a class="article" href="/ArticleRead.nhn?clubid=25474288&amp;page=1&amp;boardtype=L&amp;articleid=235073&amp;referrerAllArticles=true" onclick="clickcr(this, 'cfa.atitle','','',event);">

                    temp_dict['link'] = "https://cafe.naver.com" + x.find('a', class_="article").get('href')
                    temp_dict['name'] = x.find("td", class_="td_name").find('a', class_='m-tcol-c').text.strip()

                    try:
                        temp_dict['date'] = x.find("td", class_="td_date").text.strip().replace(".", "-")[0:-1]
                        date_str: str = temp_dict['date']
                        temp_dict.update({'date':datetime.strptime(date_str, "%Y-%m-%d")})
                    except:
                        temp_dict.update({'date': datetime.now().date()})

                    temp_dict['date'] = datetime.strftime(temp_dict['date'], "%Y-%m-%d")
                    temp_dict['view'] = x.find("td", class_="td_view").text.strip().replace(",", "")
                    if "만" in temp_dict['view']:
                        temp_dict['view'] = temp_dict['view'].replace("만", "")
                        temp_dict['view'] = temp_dict['view'].replace(".", "")
                        temp_dict['view'] = int(temp_dict['view']) * 10000
                    else:
                        temp_dict['view'] = int(temp_dict['view'])
                    db.insert("crawl_contents",
                              task_id=self.task_id,
                              author=temp_dict['name'],
                              n_view=int(temp_dict['view']),
                              post_date=temp_dict['date'],
                              url=temp_dict['link'],
                              crawl_status='F')
            print("(현재시각) " + str(datetime.now()) + ": " + str(page) + "page done")

            ### 다음 페이지로 넘어가기
            page += 1
            self.driver.implicitly_wait(1)
            try:
                if page <= 10:  # 1~10 : 페이지 번호 그대로
                    page_xpath = str(page)
                    self.driver.find_element(By.XPATH, '//*[@id="main-area"]/div[7]/a[' + page_xpath + ']').click()
                    # driver.find_element_by_xpath('//*[@id="main-area"]/div[7]/a[' + page_xpath + ']').click()
                elif page == 11:  # 11 : 다음 버튼
                    self.driver.find_element(By.XPATH, '//*[@id="main-area"]/div[7]/a[11]/span').click()
                    # driver.find_element_by_xpath('//*[@id="main-area"]/div[7]/a[11]/span').click()
                elif page > 11 and page % 10 != 1:  # 12~ : 페이지 번호 마지막 자리 + 1
                    page_xpath = str(page - ((page - 1) // 10) * 10 + 1)
                    self.driver.find_element(By.XPATH, '//*[@id="main-area"]/div[7]/a[' + page_xpath + ']').click()
                    # driver.find_element_by_xpath('//*[@id="main-area"]/div[7]/a[' + page_xpath + ']').click()
                elif page % 10 == 1:  # 21,31.. : 다음 버튼
                    self.driver.find_element(By.XPATH, '//*[@id="main-area"]/div[7]/a[12]/span').click()
                    # driver.find_element_by_xpath('//*[@id="main-area"]/div[7]/a[12]/span').click()
            except Exception as e:
                print(e)
                l = False

    def crawl_contents(self):
        self.setting()
        ### 카페 url 로 이동
        self.get_driver()
        self.driver.get(url=self.page_link)
        if self.login_required:
            ### 로그인
            self.driver.implicitly_wait(10)
            self.login()
            time.sleep(10)
        num_per_page = 15  # 페이지당 게시글 갯수(default: 15개)
        address_list = []
        page = 1

        content_rows = db.select("crawl_contents", "*", f"task_id={self.task_id} and crawl_status='F'")

        i = 0
        contents_list = []  # 내용
        reply_list = []  # 댓글
        error_list = []  # 에러난 게시글

        while True:
            ### 수집 링크로 이동
            url = content_rows[i]['url']
            contents_id = content_rows[i]['contents_id']
            self.driver.get(url)
            time.sleep(1)
            page_soup = None
            try:
                self.driver.switch_to.frame('cafe_main')
                r = self.driver.page_source
                page_soup = BeautifulSoup(r, "html.parser")
                content = page_soup.find('div', class_='ArticleContentBox')
                ### 게시글 수집
                temp_dict = {}
                temp_dict['title'] = ""
                with suppress(AttributeError):  # 제목 없는 게시글
                    temp_dict['title'] = content.find('h3', class_='title_text').text.strip()
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'article_viewer')))  # article_viewer 가 등장하기 전까지
                temp_dict['product_name'] = content.find("a", class_="link_board").text
                temp_dict['text'] = content.find("div", class_="CafeViewer").text.strip()  ##중복되는 공지글 제외
                temp_dict['text'] = temp_dict['text'].replace("\n", "")
                temp_dict['text'] = temp_dict['text'].replace("\u200b", "")
                temp_dict['crawl_status'] = "T"
                print(f"location : {temp_dict['product_name']}/ text:{temp_dict['text']}")
                db.update_multi("crawl_contents", temp_dict, {"contents_id": contents_id})
                contents_list.append(temp_dict)

                ### 댓글 수집
                if content.find("div", class_="ReplyBox") is not None:  # 댓글 기능이 아예 없음
                    comment_num = content.find("div", class_="ReplyBox").find("a", class_="button_comment").find(
                        "strong").text
                    print(f"{i}번째:댓글 수집 확인 comment_num: {comment_num}")
                    if comment_num != '0':  # 댓글이 있을떄
                        comment = content.find("div", class_="CommentBox").find("ul", class_="comment_list").select(
                            "li")

                        ### 댓글 구분
                        com_n = 0  # 댓글
                        com_nn = 0  # 대댓글
                        comment_list = []
                        for n in range(len(comment)):

                            if comment[n].get('class') == ['CommentItem']:  # 댓글
                                com_n += 1
                                com_nn = 0
                                com_thread = str(com_n) + "-" + str(com_nn)
                                com_nn = 1
                            elif comment[n].get('class') == ['CommentItem', 'CommentItem--reply']:  # 대댓글
                                com_thread = str(com_n) + "-" + str(com_nn)
                                com_nn += 1

                            ### 댓글 내용 수집
                            if comment[n].text.strip() != '삭제된 댓글입니다.':
                                com_nick = comment[n].find("a", class_="comment_nickname").text.strip()
                                com_date = comment[n].find("span", class_="comment_info_date").text.strip()
                                com_reply = comment[n].find("div", class_="comment_text_box").text.strip()
                                com_reply = com_reply.replace("\n", "").replace("\u200b", "")

                                # db.insert("crawl_contents",
                                #           author = com_nick,
                                #           task_id = task_id,
                                #           url=url,
                                #           text=com_reply,
                                #           is_reply=1)
                                com_reply_dict = {"author": com_nick, "text": com_reply}
                                comment_list.append(com_reply_dict)
                        print(f"{i}//comment_list:{comment_list}")
                        db.update_one("crawl_contents", "review", str(comment_list), "contents_id", contents_id)
                i += 1

            except Exception as e:
                print(e)
                i += 1
                continue

        #         ### 게시글을 볼 등급이 안됨
        #         if page_soup.find('strong', class_='emph') is not None:
        #             error_list.append({"error" :  page_soup.find('strong', class_='emph').text+"등급 필요"
        #                                , "url" : url})
        #             pass
        #         ### 에러 따로 확인
        #         else:
        #             error_list.append({"error" : "에러 확인 필요"
        #                                , "url" : url})
        #             pass
        # 크롬 종료