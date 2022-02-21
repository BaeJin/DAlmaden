from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .exception import *
import time
from selenium.webdriver.common.by import By
from datetime import datetime

class Crawler:
    def __init__(self, timeout=60, retry=True,headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
            options.add_argument("window-size=1920x1080")
            options.add_argument("disable-gpu")
            
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.retry = retry
        self.driver = driver
        self.driver.set_page_load_timeout(timeout)
        
    def get_post_date(self):
        try:
            post_date:str = self.driver.find_element(By.XPATH, "//span[@class ='gall_date']").text
        except:
            return None
        if post_date:
            post_date = post_date.replace(".","-")
            post_date = post_date.split(" ")[0]
            return datetime.strptime(post_date,"%Y-%m-%d").strftime("%Y-%m-%d")
    def get_nickname(self):
        try:
            nickname = self.driver.find_element(By.XPATH, "//span[@class='nickname']").text
        except Exception as e:
            print(e)
            return None
        return nickname
    def get_view_count(self):
        try:
            view_count = self.driver.find_element(By.XPATH, "//span[@class='gall_count']").text
        except Exception as e:
            print(e)
            return None
        if view_count:
            view_count = view_count.replace("조회","")
            view_count = int(view_count.strip())
        return view_count
    def get_like_count(self):
        try:
            like_count = self.driver.find_element(By.XPATH, "//span[@class='gall_reply_num']").text
        except Exception as e:
            print(e)
            return None
        if like_count:
            like_count = like_count.replace("추천","")
            like_count = int(like_count.strip())
        return like_count
    
    def crawl(self, gallery, idx,batch_size):
        while True:
            try:
                link = f"https://gall.dcinside.com/board/view/?id={gallery}&no={idx}"
                self.driver.get(link)
                try:
                    self.driver.find_element(By.CLASS_NAME,"delet")
                except NoSuchElementException:
                    pass
                else:
                    raise DeletedPostException

                comments = []
                try:
                    n_comments = self.driver.find_element(By.CLASS_NAME,"cmt_paging")
                    n_comments = n_comments.find_elements(By.TAG_NAME,"a")
                    last_comment_page = len(n_comments) + 1
                except NoSuchElementException:
                    last_comment_page = 0

                title = self.driver.find_element(By.CLASS_NAME,"title_subject")
                post_date = self.get_post_date()
                nickname = self.get_nickname()
                view_count = self.get_view_count()
                like_count = self.get_like_count()
                content = self.driver.find_element(By.CLASS_NAME,"writing_view_box")
                content = content.find_elements(By.TAG_NAME,"div")
                content = content[-1]
                if content:
                    if isinstance(content.text, str):
                        content_text = content.text.replace("\n","")
                    else:
                        content_text= None
                for i in range(last_comment_page, 0, -1):
                    self.driver.execute_script(f"viewComments({i}, 'D')")
                    page_comments = self.driver.find_elements(By.CLASS_NAME, "usertxt")
                    for comment in page_comments:
                        comments.append(comment.text)

                return {
                    "title": title.text,
                    "text": content_text,
                    "author":nickname,
                    "post_date": post_date,
                    "review": comments,
                    "n_view": view_count,
                    "n_like": like_count,
                    "url":link
                }

            except Exception as e:
                print(e)
                idx+=batch_size
                return {
                    "link": link,
                    "error": e
                }
