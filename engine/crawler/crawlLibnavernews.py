import requests
from bs4 import BeautifulSoup
import json
import pymysql
import re
from datetime import datetime
from time import sleep
import openpyxl
from engine.sql.almaden import Sql
from engine.sql.almaden import cleanse

# custom_header을 통해 아닌 것 처럼 위장하기



class CrawlLibnaverNews:
    def __init__(self,task_id=None,keyword=None,from_date=None,to_date=None,n_crawl=None,n_total=None):

        self.task_id = task_id
        self.status_done = 'GF'
        self.status_doing = 'GI'
        self.status_do = 'GR'
        self.status_error = 'ER'
        self.nCrawled = 0
        self.keyword = keyword
        self.startDate = from_date
        self.endDate = to_date
        self.nCrawl = n_crawl
        self.nTotal = n_total
        self.CUSTOM_HEADER = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'cookie': 'NNB=A6MBAJEMY62F4; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; ASID=6af6a9ce000001725f1827c70000004e; nid_inf=-1389872108; NID_JKL=n4a+gXL5eCtmK9yqbQ52fKKBbmyCNu0Tk6Ue+v3fGRc=; _ga_7VKFYR6RV1=GS1.1.1591333741.1.0.1591333741.60; _ga=GA1.1.1609373596.1590384594; BMR=s=1591584337158&r=https%3A%2F%2Fm.blog.naver.com%2Fjoytoseon%2F221949585643&r2=https%3A%2F%2Fwww.google.com%2F; _naver_usersession_=2INFMUJNtrv0an16MeMltg==; nx_ssl=2; nx_open_so=1; page_uid=UW3GCwprvxsssNREPLRssssss6d-236989',
            'referer': '',  # url
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

    def crawl_total(self):
        db = Sql('datacast2')

        clientID = 'vDMsgzbR0LTqOZPunT7w'
        client_secret = 'Fte_UsmhS6'
        keyword = self.keyword
        ##가져올 상품 갯수 설정
        display = '20'
        ##어디서부터 가져올지 설정
        start = '1'
        ##정렬 기준 설정 (sim: 유사도)
        sort = 'sim'

        params = (
            ('query', keyword),
            ('display', display),
            ('start', start),
            ('sort', sort)
        )

        ##header를 설정해준다. header 는 naver_api clientID 와 secret 을 이용
        headers = {
            'X-Naver-Client-Id': clientID,
            'X-Naver-Client-Secret': client_secret,
        }
        ##네이버쇼핑 상품 리스트 가져오기
        response = requests.get('https://openapi.naver.com/v1/search/news.json?', headers=headers, params=params)
        nTotal = int(re.sub('(<([^>]+)>)', '', str(response.json()['total'])))
        print(nTotal)
        db.update_one('crawl_task', 'n_total', int(nTotal), 'task_id', self.task_id)

    def crawl(self):
        # init task
        db = Sql('datacast2')
        keyhex = self.get_keyhex(self.keyword)
        custom_header = self.CUSTOM_HEADER


        pageNo = 1
        ban_counter = 0
        rel_news_no_count=0
        err = 0
        end = False
        previous_news_url = []
        while self.nCrawled < self.nCrawl:

            url_keyword = keyhex
            url_startDate = str(self.startDate).replace("-", ".")

            url_endDate = str(self.endDate).replace("-", ".")
            url_from = str(self.startDate).replace("-", "")
            url_to = str(self.endDate).replace("-", "")
            url_startNum = (pageNo - 1) * 10 + 1
            list_url = f"https://search.naver.com/search.naver?where=news&query={url_keyword}&sort=0&ds={url_startDate}&de={url_endDate}&nso=so%3Ar%2Cp%3Afrom{url_from}to{url_to}%2Ca%3A&start={url_startNum}"
            custom_header['referer'] = list_url
            req = requests.get(list_url, headers=custom_header)  # custom_header를 사용하지 않으면 접근 불가
            if req.status_code == requests.codes.ok:
                data_list = req.text
                r = re.compile('(?<=href=").*?(?=")')
                urls = r.findall(data_list)
                url_naver_news_list = list(filter(lambda x : x.startswith("https://news.naver.com"),urls))

                if len(url_naver_news_list) == 1:
                    previous_news_url.append(url_naver_news_list[0])
                    if len(previous_news_url)>=2:
                        for i,url in enumerate(previous_news_url):
                            print('cafeloader',previous_news_url[i-1], previous_news_url[i])
                            if previous_news_url[i-1] == previous_news_url[i]:
                                end = True
                if end ==True:
                    db.update_one('crawl_task', 'crawl_status', 'GF', 'task_id', self.task_id)
                    break

                if len(url_naver_news_list)==0 :
                    rel_news_no_count +=1

                    if rel_news_no_count<10:
                        continue
                    if rel_news_no_count>10:
                        db.update_one('crawl_task', 'crawl_status', 'GF', 'task_id', self.task_id)
                        print("해당 키워드, 기간에 대한 뉴스 기간이 없습니다.")
                        print("Process will be ended")
                        break

                for url in url_naver_news_list:

                    self.nCrawled += 1
                    try:
                        print('crawling', self.nCrawled, url)
                        custom_header['referer'] = url
                        req = requests.get(url, headers=custom_header)  # custom_header를 사용하지 않으면 접근 불가
                        ban_counter += 1
                        bs = BeautifulSoup(req.content, 'html.parser')

                        title = cleanse(
                            bs.select_one('h3#articleTitle').text)  # 대괄호는 h3 # articleTitle 인 것 중 첫번째 그룹만 가져오겠다.
                        post_date = bs.select_one('.t11').get_text()[:10].strip().replace(".", "-")  # publishtime 가져오기

                        _text = bs.select_one('#articleBodyContents').get_text().replace('\n', " ")  # 본문
                        text = cleanse(
                            _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", ""))
                        publisher = bs.select_one('#footer address').a.get_text()

                        if self.nCrawled % 100 == 0:
                            print('post Num :', self.nCrawled)
                        db.insert('crawl_contents',
                                  task_id=self.task_id,
                                  num=self.nCrawled,
                                  post_date=post_date,
                                  title=title,
                                  text=text,
                                  author=publisher,
                                  url=url
                                  )
                    except Exception as ex:
                        print(ex)
                        continue

                    if ban_counter >= 2500:
                        print("Pause crawling for 2 mins")
                        sleep(120)
                        ban_counter = 0

                    if self.nCrawled >= self.nCrawl:
                        db.update_one('crawl_task', 'n_crawled', self.nCrawled, 'task_id', self.task_id)
                        db.update_one('crawl_task', 'crawl_status', 'GF', 'task_id', self.task_id)
                        print(f"Process complete. crawled files : {self.nCrawled}")
                        break
                pageNo += 1

            else:
                err += 1
                print("request error:" + str(err))
                print("waiting 4min for re-entry")
                sleep(240)
                if err > 5:
                    print("Process ended by error")
                    end = True

            if end:
                db.update_one('crawl_task', 'n_crawled', self.nCrawled, 'task_id', self.task_id)
                db.update_one('crawl_task', 'crawl_status','GF', 'task_id', self.task_id)
                break
            print(self.nCrawled,self.task_id)
            db.update_one('crawl_task', 'n_crawled', self.nCrawled, 'task_id', self.task_id)
            if self.nCrawled >= self.nCrawl:
                db.update_one('crawl_task', 'crawl_status', 'GF', 'task_id', self.task_id)

        return self.task_id


    def get_keyhex(self,keyword):
        keyint = keyword.encode("UTF-8")
        keyhex = ""
        for i in keyint:
            keyhex = keyhex + '%{:02X}'.format(i)
        return keyhex


    # def get_reporter(self,btext):  # text 에서 기자 이름 추출하기
    #     try:
    #         index=None
    #         pharse = re.findall(r"[\w']+", btext)  # 특수문자 공백 단위로 문장 쪼개기
    #         for i, keyword in enumerate(pharse):  # 기자를 포함하는 문장을 모두 rp 에 담아준다. 기자 를 포함하는 문장중 마지막 문장이 기자 이름을 포함하기 때문에 덮어씌어준다.
    #             if keyword == '기자':
    #                 index = i
    #         rp = pharse[index - 1]
    #     except Exception as ex:
    #         return None
    #     return rp
    #

    # def get_email(self,btext):  # text 에서 기자 email 추출하기
    #     try:
    #         # 기자 email 뽑아내기
    #         email = re.findall('\S+@\S+', btext)
    #         email = email[0]
    #         email = re.sub('[가-힣]', "", email)
    #         email = re.sub('\'', '', email)
    #         email = re.sub('\"', '', email)
    #         email = re.sub('\[.*\)', "", email)
    #         email = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', "", email)
    #         email = re.sub('\-|\]|\{|\}|\(|\)*', "", email)
    #     except Exception as ex:
    #         return None
    #     return email
    #

    # def get_imageUrl(soup):
    #     try:
    #         img = soup.select('#articleBodyContents')[0]
    #         img = img.find_all("img")  # img 태그 찾기
    #         img_src_list = []
    #         for i in img:
    #             img_src = i['src']  # img 태그 중 src 속성 저장
    #             if 'http' in img_src:  # http로 소스 읽어들일 수 있는 이미지만 저장한다.
    #                 img_src_list.append(img_src)  # img 다운로드를 위해 list 에 추가한다.
    #         text = re.sub('\'', '', str(img_src_list))
    #         text = re.sub('\"', '', text)
    #         text = re.sub('\[', "", text)
    #         text = re.sub('\]', "", text)
    #     except Exception as ex:
    #         return None
    #     return text