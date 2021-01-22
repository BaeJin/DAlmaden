from sqlalchemy import create_engine
import re
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import time
from scrapy import Selector
import random
from engine.sql.almaden import Sql
import pandas as pd

API_KEY = "2c5b500fff718ba1c67f02eb21e79358"

class CrawlLibNavershopping:

    def __init__(self,task_id=None,
                 contents_id=None,
                 keyword=None,
                 from_date=None,
                 to_date=None,
                 n_crawl=None,
                 n_total=None,
                 prod_desc=None,
                 default_product_num=20):

        self.CUSTOM_HEADER = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1v485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
            'referer': 'https://cr.shopping.naver.com/adcr.nhn?x=UqdHTJoNTCLmDRJmeUnHlf%2F%2F%2Fw%3D%3Dso9VDpccOJEJRAIk8kuUlxMWrABtahSEWMaqJo3m9UbdvL12W5aYi%2FTl6p%2B3d7gt2UDGZeWTm1v%2BM3dgb6pD%2BDcA8tPryz%2FlDyJRIn%2F3GbdYxTbKPi8joU3Nl4X0DXHSo3Y9fIdJ5zZ5Cp5gsTRBKAtyGaSr%2B0dRu37W7MMIB4NGtrk2YZNI7XPUxwzPc48d9mgXdPaip9zehn8GnNDvG2V9H67KEMncnWpoX4ZNWSLk4bc4NKsfCCJHgd8ZAW%2BSc%2FLKc3OGGtGoebD6lZ4I44ISv2w0Yv0stZD6LKftbf55bUf73NilrRL4RDYk4DmFeq3btKVxhUpidTfV6BgzPrJl5ZvLlNP%2B%2FvAE%2FR15kJfy9835OhANBmT1EtNrHhr2FCt5YK%2FmGsUxO25%2F2s6FZQcOmY27ZGze0Q%2BtXRlM4OxtarJoVrbEtunAYIkKGowOqukzgPDVXo6AvL8aV8tkrWSEhb%2B5%2BbgCLWD5ufmjwVaC0c1bmOP2u2YumOF3Sc7ORjT3CA11g7crAXPKtuqjMF6AhfbmRc6T9Q91MqoVII6q9tyiYebOu2HANWNhP0a1Sk4qXti8zVzVPIzmwp4FnMxjpTF8mUvzAqbc%2BYg0Db%2FqzD%2B13y5qA3088r1MNA5Dgw2popvk5HxytjbrmvguYxNgCgu8TH6IETI9IR%2BJIKXeXzoAYWtugk3VcH2L2xPlsYFx8Zt3N1gkRM4V7K6KABgau4fTwOUqyF63FjwpQRls%3D&nvMid={}&catId=50001986',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.engine = create_engine(
            ("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8").format
            ('root',
             'robot369',
             '1.221.75.76',
             3306,
             'datacast'),
            encoding='utf-8'
            )
        self.db = Sql("datacast2")
        self.task_id = task_id
        self.contents_id = contents_id
        self.keyword = keyword
        self.from_date = from_date
        self.to_date = to_date
        self.n_crawl = n_crawl
        self.n_total = n_total
        self.prod_desc = prod_desc
        self.merged_dict = {}
        self.channel = 'navershopping'
        self.default_product_num = default_product_num
        self.n_crawled = 0
    # def get_product_info_list_to_crawl(self):
    #     tasks_df = pd.DataFrame(columns=['from_date','to_date','keyword','channel','n_crawl','task_memo'])
    #     contents_df = pd.DataFrame(columns=['title', 'to_date', 'keyword', 'channel', 'n_crawl', 'task_memo'])
    #
    #     product_info_list = self.get_product_page_info()
    #     for index, product_info in enumerate(product_info_list):
    #         product_name = product_info["title"]
    #         tasks_df.at[index,'n_crawl'] = self.n_crawl
    #         tasks_df.at[index,'task_memo'] = json.dumps(product_info,ensure_ascii=False)
    #     return tasks_df,contents_df

    # def crawl(self):
    #     product_info_list = self.get_product_page_info()
    #     for index, product_info in enumerate(product_info_list):
    #         product_name = product_info["title"]
    #         product_info = json.dumps(product_info,ensure_ascii=False)
    #         print(product_info)
    #         self.db.insert("crawl_contents",
    #                        task_id=self.task_id,
    #                        text=product_info,
    #                        title=product_name)
    #         print(index, product_info)
    def get_url(self, target_url):
        url = f"http://api.scraperapi.com?api_key={API_KEY}&url={target_url}"
        return url
    def get_product_info_by_api(self):
        clientID = 'vDMsgzbR0LTqOZPunT7w'
        client_secret = 'Fte_UsmhS6'
        keyword = self.keyword
        ##가져올 상품 갯수 설정
        ##어디서부터 가져올지 설정
        start = '1'
        display = self.default_product_num
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
        response = requests.get('https://openapi.naver.com/v1/search/shop.json?', headers=headers, params=params)

        return response

    def crawl_total(self):
        response = self.get_product_info_by_api()
        self.crawl_total_product_count(response)
        self.crawl_total_review_count(response)

    def crawl_total_product_count(self,response):
        db = Sql('datacast2')
        nTotal = int(re.sub('(<([^>]+)>)', '', str(response.json()['total'])))
        print(self.keyword,'task_id:',self.task_id,"nTotal:",nTotal)
        db.update_one('crawl_task', 'n_total', int(nTotal), 'task_id', self.task_id)

    def crawl_total_smartstore_count(self,response):
        final_product_list = self.get_product_page_info(response)
        for product_info in final_product_list:
            if product_info['type'] == 'smartstore':
                # product info 를 이용해서 review page 정보 만들기
                review_page_info = self.get_review_smartstore_page_info(product_info)
                print(review_page_info['review_amount'],review_page_info['sale_amount'],product_info['link'])


    def crawl_total_review_count(self,response):
        print('review count 시작')
        final_product_list = self.get_product_page_info(response)
        for product_info in final_product_list:
            if product_info['type'] == 'smartstore':
                # product info 를 이용해서 review page 정보 만들기
                review_page_info = self.get_review_smartstore_page_info(product_info)
                product_info['sale_amount'] = review_page_info['sale_amount']
                contents_id = self.db.insert_withoutDuplication('crawl_contents',
                               ['title','task_id'],
                               title=product_info['title'],
                               task_id=float(self.task_id),
                               text=json.dumps(product_info,ensure_ascii=False),
                               n_reply=review_page_info['review_amount'],
                               crawl_status="GR")


            if product_info['type'] == 'navershopping':
                product_link = product_info['product_link']
                response = requests.get(product_link)
                soup = BeautifulSoup(response.text,'lxml')
                page_data = soup.find('script', {'id': '__NEXT_DATA__'}).string
                page_data_json = json.loads(page_data)
                product_review_count = page_data_json["props"]["pageProps"]["initialState"]["catalog"]["info"]["reviewCount"]
                contents_id = self.db.insert_withoutDuplication('crawl_contents',
                               ['title', 'task_id'],
                               title = product_info['title'],
                               task_id=float(self.task_id),
                               text=json.dumps(product_info,ensure_ascii=False),
                               n_reply=product_review_count,
                               crawl_status="GR")
            else:
                print('response:',response.status_code)
    def get_type_of_url_from_gate(self, navershopping_api_product_link_gate):
        counter = 0
        while True:
            cond = False
            navershopping_api_product_link_body = requests.get(navershopping_api_product_link_gate)
            if navershopping_api_product_link_body.status_code == 200:
                cond = True
            elif counter >= 5:
                navershopping_api_product_link_body = requests.get(self.get_url(navershopping_api_product_link_gate))
            else:
                counter += 1
                time.sleep(10)
            if cond:
                return navershopping_api_product_link_body

    def get_product_page_info(self,response):
        response = re.sub('(<([^>]+)>)', '', str(response.json()['items']))

        response = response.replace("\'","\"")
        response = re.sub(r'\\x..','',response)
        response_json = json.loads(response)
        final_product_list = []
        for idx,i in enumerate(response_json):
            navershopping_api_product_link_gate = i['link']
            navershopping_api_product_link_body = self.get_type_of_url_from_gate(navershopping_api_product_link_gate)
            navershopping_api_product_link_list = re.findall('\((.*?)\)',navershopping_api_product_link_body.text)
            navershopping_api_product_link = navershopping_api_product_link_list[0]
            product_link = navershopping_api_product_link.replace("'","")

            if product_link.startswith('https://smartstore.naver.com/'):
                final_product_link = product_link
                container_dict = {'type': 'smartstore','product_link':final_product_link,'productId':i['productId']}
            elif product_link.startswith('/detail/detail'):
                product_link = product_link.replace('=','/').replace('&','/').replace('?','/')
                product_link = product_link.split('/')
                cat_id = product_link[4]
                mid = product_link[6]
                final_product_link='https://search.shopping.naver.com/catalog/{}?cat_id={}&nv_mid={}'.format(mid,cat_id,mid)
                container_dict = {'type': 'navershopping','product_link':final_product_link,'productId':i['productId']}

            else:
                container_dict = {'type': 'other','product_link':i['link'],'productId':i['productId']}
            self.merged_dict = {**i,**container_dict}
            final_product_list.append(self.merged_dict)
        return final_product_list



    def get_review_navershopping_page_info(self,product_info):
        self.CUSTOM_HEADER = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1v485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
            'referer': 'https://cr.shopping.naver.com/adcr.nhn?x=UqdHTJoNTCLmDRJmeUnHlf%2F%2F%2Fw%3D%3Dso9VDpccOJEJRAIk8kuUlxMWrABtahSEWMaqJo3m9UbdvL12W5aYi%2FTl6p%2B3d7gt2UDGZeWTm1v%2BM3dgb6pD%2BDcA8tPryz%2FlDyJRIn%2F3GbdYxTbKPi8joU3Nl4X0DXHSo3Y9fIdJ5zZ5Cp5gsTRBKAtyGaSr%2B0dRu37W7MMIB4NGtrk2YZNI7XPUxwzPc48d9mgXdPaip9zehn8GnNDvG2V9H67KEMncnWpoX4ZNWSLk4bc4NKsfCCJHgd8ZAW%2BSc%2FLKc3OGGtGoebD6lZ4I44ISv2w0Yv0stZD6LKftbf55bUf73NilrRL4RDYk4DmFeq3btKVxhUpidTfV6BgzPrJl5ZvLlNP%2B%2FvAE%2FR15kJfy9835OhANBmT1EtNrHhr2FCt5YK%2FmGsUxO25%2F2s6FZQcOmY27ZGze0Q%2BtXRlM4OxtarJoVrbEtunAYIkKGowOqukzgPDVXo6AvL8aV8tkrWSEhb%2B5%2BbgCLWD5ufmjwVaC0c1bmOP2u2YumOF3Sc7ORjT3CA11g7crAXPKtuqjMF6AhfbmRc6T9Q91MqoVII6q9tyiYebOu2HANWNhP0a1Sk4qXti8zVzVPIzmwp4FnMxjpTF8mUvzAqbc%2BYg0Db%2FqzD%2B13y5qA3088r1MNA5Dgw2popvk5HxytjbrmvguYxNgCgu8TH6IETI9IR%2BJIKXeXzoAYWtugk3VcH2L2xPlsYFx8Zt3N1gkRM4V7K6KABgau4fTwOUqyF63FjwpQRls%3D&nvMid={}&catId=50001986',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        review_page_info = {}
        if product_info['type'] == 'navershopping':

            review_page_info['referer'] = self.CUSTOM_HEADER['referer'].format(product_info['productId'])
            review_page_info['nv_mid'] = product_info['productId']
            review_page_info['product_link'] = 'https://search.shopping.naver.com/detail/review_list.nhn'
            return review_page_info

    def get_review_smartstore_page_info(self,product_info):
        review_page_info = {}
        if product_info['type'] == 'smartstore':
            # 해당하는 url 에서 review 추출하기
            product_link = product_info['product_link']
            self.CUSTOM_HEADER['referer'] = 'https://smartstore.naver.com/'
            res_product_page = requests.get(product_link, headers=self.CUSTOM_HEADER)
            html_source_product_page = res_product_page.text
            soup_product_page = BeautifulSoup(html_source_product_page, 'lxml')
            # referer url 은 script 태그 안에 type 속성 (속성값: application/ld+json) 에 들어있음.
            # reivew 크롤링을 위해 필요한 준비사항
            # 1.page_referer_url #2.machandise_no #3.new_product_no #4.origin_product_no
            page_referer_url = None
            machandise_no = None
            new_product_no = None
            origin_product_no = None
            page_ld_json = None
            sale_amount = None
            review_amount = None
            try:
                page_ld_json = soup_product_page.find('script', {'type': 'application/ld+json'})
            except:
                print('page_ld_json is None')
            try:
                ##현재 referer url 가져오기 위한 작업 1. 태그 내의 text 를 json 으로 변환시키고 url 값만 가져온다.
                page_ld_json_to_text = page_ld_json.text
                page_info_json = json.loads(page_ld_json_to_text)

                page_referer_url = page_info_json['offers']['url']
                new_product_no = page_info_json['productID']
            except:
                pass
            try:
                # original product no 가져오기
                script_json = soup_product_page.find('script', text=re.compile("window.__PRELOADED_STATE__="))
                origin_json = str(script_json)[
                              str(script_json).find('window.__PRELOADED_STATE__='):str(script_json).find('module={}')]
                origin_json = origin_json.replace("</script", "")
                origin_json = json.loads(origin_json.replace('window.__PRELOADED_STATE__=', ''))
                machandise_no = origin_json['smartStore']['channel']['payReferenceKey']
                origin_product_no = origin_json['product']['A']['productNo']
                sale_amount = origin_json['product']['A']['saleAmount']['cumulationSaleCount']
                review_amount = origin_json['product']['A']['reviewAmount']['totalReviewCount']
            except:
                print('product:', product_info, ' error(s) occur')

            review_product_no = new_product_no if origin_product_no is None else origin_product_no
            machandise_no = machandise_no

            self.CUSTOM_HEADER['referer'] = page_referer_url
            review_page_info['sale_amount'] = sale_amount
            review_page_info['review_amount'] = review_amount
            review_page_info['referer'] = page_referer_url
            review_page_info['review_product_no'] = review_product_no
            review_page_info['machandise_no'] = machandise_no
        return review_page_info



    def crawl(self):
        prod_desc = self.prod_desc
        if prod_desc['type'] == 'smartstore':
            print("smartstore")
            # product info 를 이용해서 review page 정보 만들기
            review_page_info = self.get_review_smartstore_page_info(prod_desc)
            review_page_referer = review_page_info['referer']
            review_product_no = review_page_info['review_product_no']
            review_machandise_no = review_page_info['machandise_no']
            self.CUSTOM_HEADER['referer'] = review_page_referer
            ###리뷰 크롤링 시작
            page = 1
            retry = 0

            while self.n_crawled < min(self.n_crawl,self.n_total):
                print("self.n_crawled:",self.n_crawled, self.n_crawl, self.n_total)
                review_page_url = 'https://smartstore.naver.com/i/v1/reviews/paged-reviews?page={}&pageSize=20&merchantNo={}&originProductNo={}&sortType=REVIEW_RANKING'. \
                    format(page, review_machandise_no, review_product_no)
                res_review_page = requests.get(review_page_url, headers=self.CUSTOM_HEADER)
                if res_review_page.status_code == requests.codes.ok:
                    try:
                        res_review_page_json = res_review_page.json()
                        reviews = res_review_page_json['contents']
                        print(reviews)
                    except:
                        retry += 1
                        continue
                    retry = 0
                    for index, review in enumerate(reviews):
                        item = {}
                        self.n_crawled += 1
                        self.db.update_one("crawl_contents","n_reply_crawled",self.n_crawled,"contents_id",self.contents_id)
                        author = review["writerMemberMaskedId"]
                        review_post_date = review["createDate"].split('T')[0]
                        review_post_time = review_post_date + ' ' + review["createDate"].split('T')[1].split('.')[0]
                        rating = review["reviewScore"]
                        item["text"] = str(review["reviewContent"]).replace("\n"," ")

                        self.db.insert("crawl_sentence",
                                       contents_id=self.contents_id,
                                       seq=int(self.n_crawled),
                                       text=item["text"],
                                       rating=rating,
                                       author=str(author),
                                       sentence_post_date=review_post_date,
                                       sentence_post_time=review_post_time,
                                       sentence_type="review")
                    page += 1
                    # item["selectedOption"]

        if prod_desc['type'] == 'navershopping':
            print('navershopping')
            formdata = {'nvMid': None, 'page': 1, 'reviewSort': 'accuracy', 'reviewType': 'all','ligh': 'true'}

            review_page_info = self.get_review_navershopping_page_info(prod_desc)
            review_page_nv_mid = review_page_info['nv_mid']
            review_page_link = review_page_info['product_link']
            self.CUSTOM_HEADER['referer'] = self.CUSTOM_HEADER['referer'].format(review_page_nv_mid)
            formdata['nvMid'] = review_page_nv_mid
            page = 1
            retry = 0
            while self.n_crawled < min(self.n_crawl,self.n_total):
                print("self.n_crawled:",self.n_crawled, self.n_crawl, self.n_total)
                formdata['page'] = page
                time.sleep(random.random())
                res_review_page = requests.post(review_page_link, data=formdata, headers= self.CUSTOM_HEADER)
                if res_review_page.status_code == requests.codes.ok:
                    try:
                        soup = BeautifulSoup(res_review_page.text, 'html.parser')

                        reviews = soup.select(".atc_area")
                    except:
                        retry += 1
                        continue
                    if len(reviews) < 1: break
                    for review in reviews:
                        try:
                            self.n_crawled += 1
                            item = {}
                            selector = Selector(text=str(review.contents))
                            item["text"] = selector.css('div.atc::text').extract()
                            item["text"] = " ".join(item["text"])
                            item["postInfo"] = selector.css('.info_cell::text').extract()
                            item["rating"] = selector.css('.curr_avg strong::text').extract()
                            item["rating"] = float(item["rating"][0]) if item["rating"] is not None else None
                            author = item["postInfo"][1]
                            review_post_time = str(20)+str(item["postInfo"][2])[:-1].replace(".","-")

                            self.db.update_one("crawl_contents", "n_reply_crawled", self.n_crawled, "contents_id",self.contents_id)
                            self.db.insert("crawl_sentence",
                                           contents_id=self.contents_id,
                                           seq=int(self.n_crawled),
                                           text=item["text"],
                                           rating=item["rating"],
                                           author = str(author),
                                           sentence_post_date=review_post_time,
                                           sentence_type = "review")
                        except:
                            continue
                    page += 1
                        # item["selectedOption"]
        # else:
        #     self.db.update_one("crawl_contents", "crawl_status","ER", "contents_id", self.contents_id)
        #     return
        self.db.update_one("crawl_contents", "crawl_status", "GF", "contents_id", self.contents_id)


