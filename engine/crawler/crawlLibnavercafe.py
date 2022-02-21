from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from time import sleep
from engine.sql.almaden import Sql
from engine.sql.almaden import cleanse
from cafeloader.exceptions import *
class CrawlLibnaverCafe:

    def __init__(self,task_id,keyword, from_date, to_date, n_crawl=None,n_total=None):
        self.task_id = task_id
        self.status_done = 'GF'
        self.status_doing = 'GI'
        self.status_do = 'GR'
        self.status_error = 'ER'
        self.keyword:str = keyword
        self.startDate = from_date
        self.endDate = to_date
        self.nCrawl = int(n_crawl)
        self.nTotal = n_total
        self.CUSTOM_HEADER ={'accept': 'application/json, text/plain, */*',
                            'accept-encoding': 'gzip, deflate, br',
                            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                            'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
                            'referer': 'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword=',#+heyhex
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.keyhex = self.get_keyhex(self.keyword)
    def crawl_total(self):
        db = Sql('datacast2')
        print(f"self.keyword:{self.keyword}")
        parser_keyword = self.keyword.replace(" ","")
        headers = {
            'authority': 'apis.naver.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'accept': 'application/json, text/plain, */*',
            'x-cafe-product': 'pc',
            'content-type': 'application/json;charset=UTF-8',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://section.cafe.naver.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://section.cafe.naver.com/ca-fe/home/search/articles?q={self.get_keyhex(self.keyword)}&em=1',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        page = 1

        self.startDate = str(self.startDate).replace("-","")
        self.endDate = str(self.endDate).replace("-","")
        data = {"query": f"{self.keyword}", "page": page, "sortBy": 0, "exceptMarketArticle": 1,
                "period": [self.startDate, self.endDate]}
        response = requests.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles', headers=headers,
                                 json=data)
        json_data = json.loads(response.text)
        total_content = json_data["message"]["result"]["totalCount"]
        db.update_one('crawl_task', 'n_total', total_content, 'task_id', self.task_id)

    def get_keyhex(self,keyword) :
        keyint = keyword.encode("UTF-8")
        keyhex = ""
        for i in keyint:
            keyhex = keyhex + '%{:02X}'.format(i)
        return keyhex
    def crawl(self):
        #init task
        db = Sql('datacast2')
        db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_doing), 'task_id', self.task_id)
        nTotal = 0
        num = 0
        pageNo = 1
        ban_counter = 0
        err = 0
        end = False
        self.startDate = self.startDate.strftime("%Y-%m-%d").replace("-", "")
        self.endDate = self.endDate.strftime("%Y-%m-%d").replace("-", "")
        print(self.startDate, self.endDate)
        headers = {
            'authority': 'apis.naver.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'accept': 'application/json, text/plain, */*',
            'x-cafe-product': 'pc',
            'content-type': 'application/json;charset=UTF-8',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://section.cafe.naver.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://section.cafe.naver.com/ca-fe/home/search/articles?q={self.keyhex}&em=1',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        crawl_number = min(self.nCrawl, self.nTotal)
        print(num, crawl_number)
        while num < crawl_number:
            data = {"query": f"{self.keyword}", "page": pageNo, "sortBy": 0, "exceptMarketArticle": 1,
                    "period": [self.startDate, self.endDate]}

            response = requests.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles', headers=headers, json=data)
            json_data = json.loads(response.text)
            data_list = json_data["message"]["result"]["searchResultArticle"]["searchResult"]

            if response.status_code == requests.codes.ok:
                for data in data_list:
                    try:
                        url = data["linkUrl"]
                        response = requests.get(url)
                        bs = BeautifulSoup(response.text, "lxml")
                        iframe_url = self.get_iframe_content_url(bs)
                        content_response = requests.get(url=iframe_url, params={"useCafeId": True, "requestFrom": "A"})
                        json_data = json.loads(content_response.text)

                        text = self.get_text(json_data)
                        comment = self.get_comments(json_data)

                        #####raw result
                        all_text = text + comment
                        view = self.get_view(json_data)
                        comment_number = self.get_comment_number(json_data)
                        title = self.get_title(json_data)
                        post_date = self.get_post_date(json_data)
                        author = self.get_author(json_data)

                        print('crawling',num, url)
                        db.insert('crawl_contents',
                                  task_id=self.task_id,
                                  num=num,
                                  n_view=view,
                                  n_reply=comment_number,
                                  post_date=post_date,
                                  title=title,
                                  text=all_text,
                                  author=author,
                                  url=url
                                  )
                    except Exception as ex:
                        print(ex)
                    else:
                        num += 1
                pageNo += 1

        db.update_one('crawl_task', 'n_crawled', num, 'task_id', self.task_id)
        db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_done), 'task_id', self.task_id)

    def get_keyhex(self, keyword):
        keyint = keyword.encode("UTF-8")
        keyhex = ""
        for i in keyint:
            keyhex = keyhex + '%{:02X}'.format(i)
        return keyhex
    def get_iframe_content_url(self,bs):
        try:
            iframe_content_list = bs.find_all("script", {"type": "text/javascript"})
            iframe_content = list(
                filter(lambda x: "//cafe.naver.com/ArticleRead.nhn?" in x.get_text(), iframe_content_list))
            iframe_content = iframe_content[0]
            iframe_text = iframe_content.get_text()
            iframe_text = iframe_text.split('$("cafe_main").src = "')[1]
            iframe_text = iframe_text.split('";')[0]
            article_number = iframe_text.split("art=")[0]
            article_number = article_number.split("articleid=")[1]
            article_number = article_number.split("&")[0]
            iframe_text = iframe_text.split("art=")[1]
            iframe_segment = iframe_text.split("&clubid=")
            iframe_url = f"https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{iframe_segment[1]}/articles/{article_number}?query=&art={iframe_segment[0]}"
            return iframe_url
        except Exception as e:
            print("get_iframe_content_error:", e)
            raise GetIframeContentError()
    def get_text(self, json_data):
        content_html = json_data["result"]["article"]["contentHtml"]
        bs_content = BeautifulSoup(content_html, "lxml")
        text = bs_content.get_text()
        text = text.replace("\n", "")
        text = text.replace("\r", "")
        text = text.replace("\t", "")
        return text
    def get_title(self, json_data):
        title = json_data["result"]["article"]["subject"]
        return title
    def get_view(self, json_data):
        view = json_data["result"]["article"]["readCount"]
        return view

    def get_comment_number(self, json_data):
        comment_number = json_data["result"]["article"]["commentCount"]
        return comment_number

    def get_comments(self, json_data):
        items = json_data["result"]["comments"]["items"]
        comment = ""
        for item in items:
            comment += item["content"] if "추천인" not in item["content"] else ""
        return comment

    def get_post_date(self, json_data):
        post_date = json_data["result"]["article"]["writeDate"]
        post_date = datetime.fromtimestamp(int(post_date) / 1000)
        post_date = post_date.strftime("%Y-%m-%d")
        return post_date

    def get_author(self, json_data):
        nickname = json_data["result"]["article"]["writer"]["nick"]
        return nickname




