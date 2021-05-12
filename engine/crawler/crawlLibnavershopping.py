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
from engine.sql.almaden import cleanse, remove_tags
import pandas as pd
from urllib.request import urlopen
import re


API_KEY = "2c5b500fff718ba1c67f02eb21e79358"

class CrawlLibNavershopping:

    def __init__(self,task_id=None,
                 contents_id=None,
                 keyword=None,
                 n_total=None,
                 prod_desc=None,
                 cate_id = None,
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
        self.n_total = n_total
        self.prod_desc = prod_desc
        self.merged_dict = {}
        self.channel = 'navershopping'
        self.default_product_num = default_product_num
        self.n_crawled = 0
        self.cate_id = cate_id
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
    def get_product_info_by_api(self,idx):
        cookies = {
            'NRTK': 'ag#all_gr#1_ma#-2_si#0_en#0_sp#0',
            'NNB': 'GFWKWAX5XD2V6',
            'page_uid': 'U/TG/wp0JXossapGcNlssssstKK-151463',
            'nx_ssl': '2',
        }

        headers = {
            'authority': 'ssl.pstatic.net',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'script',
            'referer': 'https://search.shopping.naver.com/search/all?frm=NVSHTTL&origQuery=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&pagingIndex=1&pagingSize=40&productSet=total&query=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&sort=rel&timestamp=&viewType=list',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; _shopboxeventlog=false; NNB=GFWKWAX5XD2V6; page_uid=U/TG/wp0JXossapGcNlssssstKK-151463; nx_ssl=2; AD_SHP_BID=4; spage_uid=U%2FTG%2Fwp0JXossapGcNlssssstKK-151463',
            'Referer': 'https://search.shopping.naver.com/search/all?frm=NVSHTTL&origQuery=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&pagingIndex=1&pagingSize=40&productSet=total&query=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&sort=rel&timestamp=&viewType=list',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'if-none-match': '"3fa6-5b68dcea33640-gzip"',
            'if-modified-since': 'Wed, 16 Dec 2020 05:04:17 GMT',
            'urlprefix': '/api',
            'If-None-Match': '"rBZoLV4WqM2wAfbdh0VfwNSAj/8="',
            'Connection': 'keep-alive',
            'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'image',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://search.shopping.naver.com',
            'pragma': 'no-cache',
            'Origin': 'https://search.shopping.naver.com',
        }
        params = {'frm': 'NVSHTTL',
                  'pagingIndex': idx,
                  'pagingSize': '100',
                  'productSet': 'total',
                  'query': self.keyword,
                  'catId': self.cate_id,
                  'sort': 'rel',
                  'viewType': 'list'
                  }
        if self.cate_id is not None:
            del params['query']
            response = requests.get('https://search.shopping.naver.com/search/category', headers=headers, params=params,
                                    cookies=cookies)
        else:
            response = requests.get('https://search.shopping.naver.com/search/all', headers=headers, params=params, cookies=cookies)
        print(params)
        return response

    def crawl_total(self):
        db = Sql("datacast2")
        request = db.select('crawl_request AS cr '
                            'JOIN crawl_request_task AS crt ON cr.request_id= crt.request_id '
                            'JOIN crawl_task AS ct ON ct.task_id = crt.task_id', what='cr.category_id',
                            where=f'ct.task_id={self.task_id}')
        print("task_id:",self.task_id)
        self.cate_id = request[0]['category_id'] if request[0]['category_id'] is not None else None

        n_total = self.crawl_total_product_count()
        self.crawl_product_list(n_total)

    def crawl_total_product_count(self):
        response = self.get_product_info_by_api(1)

        db = Sql('datacast2')
        data_to_json = json.loads(response.text)
        nTotal = data_to_json['shoppingResult']['total']
        db.update_one('crawl_task', 'n_total', int(nTotal), 'task_id', self.task_id)
        return nTotal

    def get_product_character_value(self,product_info):
        ##attributeValue 를 가져오는 작업
        characterValue_data = {}
        keys = product_info['attributeValue'].split("|")
        values = product_info['characterValue'].split("|")
        for idx2, key in enumerate(keys):
            if key not in characterValue_data.keys():
                characterValue_data[key] = values[idx2]
            else:
                characterValue_data[key] += ',' + values[idx2]
        for key in characterValue_data.keys():
            characterValue_data[key] = characterValue_data[key].split(",")
        return characterValue_data

    def crawl_product_list(self,n_total):
        n_total = min(n_total,8100)
        iternum = (n_total//100)+1
        for iter in range(1,iternum+1):
            response = self.get_product_info_by_api(iter)
            data_to_json = json.loads(response.text)
            products_info = data_to_json['shoppingResult']['products']
            for idx, product_info in enumerate(products_info):
                characterValue_data = self.get_product_character_value(product_info)
                prod_desc = {
                          'rank':product_info['rank'],
                          'type':self.get_product_type(product_info),
                          'sale_amount':product_info['purchaseCnt'],
                          'title':product_info['productTitle'],
                          'category1':product_info['category1Name'],
                          'category2':product_info['category2Name'],
                          'category3':product_info['category3Name'],
                          'category4':product_info['category4Name'],
                          'brand':product_info['brand'],
                          'maker':product_info['maker'],
                          'lprice':product_info['lowPrice'],
                          'hprice':product_info['highPrice'],
                          'reviewCount':product_info['reviewCount'],
                          'post_date':product_info['openDate'],
                          'price':product_info['price'],
                          'keepCnt':product_info['keepCnt'],
                          'image':product_info['imageUrl'],
                          'link':product_info['crUrl'],
                          'productId':product_info['id'],
                          'characterValue':characterValue_data,
                          'product_link': self.get_product_link(product_info)}

                self.db.insert('crawl_contents',
                                num=(iter-1)*100 +idx,
                                title =product_info['productTitle'],
                                product_name = product_info['productTitle'],
                                task_id=float(self.task_id),
                                text=json.dumps(prod_desc,ensure_ascii=False),
                                n_reply=product_info['reviewCount'],
                                sale_amount = product_info['purchaseCnt'],
                                crawl_status='GR',
                                url = self.get_product_link(product_info),
                                img_url = product_info['imageUrl']
                               )

    def get_product_type(self,product_info):
        #navershopping
        if len(product_info['mallProductUrl']) == 0:
            return 'navershopping'
        #smartstore
        elif 'smartstore' in product_info['mallProductUrl']:
            return 'smartstore'
        #othershopping
        else:
            return 'otherChannel'

    def get_product_link(self,product_info):
        #navershopping
        if len(product_info['mallProductUrl']) == 0:
            return product_info['crUrl']
        #smartstore
        elif 'smartstore' in product_info['mallProductUrl']:
            return product_info['mallProductUrl']
        #othershopping
        else:
            return product_info['mallProductUrl']
        pass

    def get_review_navershopping_page_info(self,product_info):
        self.CUSTOM_HEADER = {
                'authority': 'search.shopping.naver.com',
                'sec-ch-ua': '^\\^',
                'accept': 'application/json, text/plain, */*',
                'urlprefix': '/api',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://cr.shopping.naver.com/adcr.nhn?x=j12fA6ihnGNtkC0ZYyCGKv%2F%2F%2Fw%3D%3Ds%2BPsiHxQXuMpn4YuUSgrUOcmqEiq6OjrFN1rHlQHnch7zSOmTS42enKYm3kPOXLHl8WHA5RjWLfCN827qYWLHr1URgynFkMa1iEW7imT2D0TDpmNu2Rs3tEPrV0ZTODsb7JQtrMqSgEftbsAH7BzOjn7C8oLNURiEaE%2BZtoYBPlsi2D9FHsVFihtMV9WFYwR1gRokOxYiLF7s%2FPq4uTtLld9%2BKy%2Fm0d%2BgYWHtEf61Jo5CNclKwvLyA%2Fys%2F%2FHPPajLvZMdfslqBv6%2FzdsDQYyIaZK8LJLETsngefeCP0Z8nADPRx1i%2Bp%2Bk3hzlMJYFt6hqQxCjRgmCDthdtiT59JO9yovxjvDZ9umtgd6xeTqAA1hIAJ%2FJQ9vsa4G5awamMD3Visext5K2yYkF868rsMDqia%2BT6ZCOywRPfbjm%2FYdPAcwczY%2F8eCyfgopyQ9U22UU99UEMwi63jafLIzwwY0rYsbF%2Fh0Ht2fYRw5EqsonD2ydFUy6EAFE5jC7zg90uEgyjRYgXT8U0rr2Dm%2BuxQGAQBpSxfHDaV%2FO9PnQ2QqUCBx%2BYGVIpQWroqD6P8QiVmqU6sL8NsZuLrYcQe2suKiuA6WA2glWH1TKancJct29CHzqS9Of8p6VybKDDhGhaLORhRaWWQNozKbzfxBdqVYoTDXxSiGQZZq6WCPHj0EuB%2FU7ipqOSBSwGxwKjkzX1yddaB1jb8xDmz4mgtOb1rvGj1B6ZE%2BX0yPcxmdCnIlN0Vf4GruH08DlKshetxY8KUEZb&nvMid=26703328400&catId=50004666',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'NNB=RCAFITJ45R3GA; nx_ssl=2; AD_SHP_BID=24; pc_ranking_info=Y; NaverSuggestUse=unuse^%^26use; sus_val=h1lAk0woMFe7EVmMrppte8he; spage_uid=; ncpa=432352^|kol5wryw^|21f05720b79566d6ed5bdb6cbedddc1bb2b06caa^|s_28826208103388785^|f9eb24d2c2ce4413ee83818ab25a5c3d686f7324:1121368^|kol6511c^|a2489873a3bb09c469ebaec6819a7d2e1fddcf48^|s_2b4a1d3455e31^|5b51e0d0be1cc5c4532a083c16eb7ff37102986a:95694^|kol6544g^|f52b2dfd51115c2bc90d2084edd5aff78ac1fa4d^|null^|ae4ba32fac88e655ab563b02aaa3fdf74206f3b3',
            }

        review_page_info = {}
        if product_info['type'] == 'navershopping':

            review_page_info['referer'] = product_info['link']
            review_page_info['nv_mid'] = product_info['productId']
            review_page_info['product_link'] = "https://search.shopping.naver.com/review"
            return review_page_info

    def get_review_smartstore_page_info(self,product_info):
        review_page_info = {}
        if product_info['type'] == 'smartstore':
            # 해당하는 url 에서 review 추출하기
            product_link = product_info['product_link']
            self.CUSTOM_HEADER['referer'] = 'https://smartstore.naver.com/'
            try:
                res_product_page = requests.get(product_link, headers=self.CUSTOM_HEADER)
            except Exception as e:
                print(e,"smartstore crawling requesst erorr, we rotate proxy")
                while True:
                    res_product_page = requests.get(self.get_url(product_link), headers=self.CUSTOM_HEADER)
                    if res_product_page.status_code==200:
                        print('roatating proxy success')
                        break
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
                new_product_no = page_info_json['productId']
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

            while self.n_crawled < self.n_total:
                print("self.n_crawled:", self.n_crawled, self.n_total)
                review_page_url = 'https://smartstore.naver.com/i/v1/reviews/paged-reviews?page={}&pageSize=20&merchantNo={}&originProductNo={}&sortType=REVIEW_RANKING'. \
                    format(page, review_machandise_no, review_product_no)
                try:
                    res_review_page = requests.get(review_page_url, headers=self.CUSTOM_HEADER)
                except Exception as e:
                    print(e, "review crawling request error we rotate proxy")
                    while True:
                        try:
                            res_review_page = requests.get(self.get_url(review_page_url), headers=self.CUSTOM_HEADER)
                            if res_review_page.status_code == 200:
                                print('review crawling request sucess,','roatating proxy success')
                                break
                        except:
                            pass
                if res_review_page.status_code == requests.codes.ok:
                    try:
                        res_review_page_json = res_review_page.json()
                        reviews = res_review_page_json['contents']
                        print("len(reviews):",len(reviews))
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
            review_page_info = self.get_review_navershopping_page_info(prod_desc)
            self.CUSTOM_HEADER['referer'] = review_page_info['referer']
            review_page_nv_mid = review_page_info["nv_mid"]
            review_page_link = review_page_info["product_link"]
            page = 1
            retry = 0

            while self.n_crawled < self.n_total:
                print("self.n_crawled:", self.n_crawled, self.n_total)
                params = {'nvMid': review_page_nv_mid, 'page': page, 'page_size': 30, 'sort': 'QUALITY',
                          'reviewType': 'ALL'}
                time.sleep(random.random())

                res_review_page = requests.get(review_page_link, params=params, headers= self.CUSTOM_HEADER)
                if res_review_page.status_code == requests.codes.ok:
                    try:
                        review_data_list = res_review_page.json()['reviews']
                    except:
                        retry += 1
                        continue
                    if len(review_data_list) < 1: break
                    for review in review_data_list:

                        try:
                            self.n_crawled += 1
                            self.db.update_one("crawl_contents", "n_reply_crawled", self.n_crawled, "contents_id",self.contents_id)
                            self.db.insert("crawl_sentence",
                                           contents_id=self.contents_id,
                                           seq=int(self.n_crawled),
                                           text=remove_tags(review["content"]),
                                           rating=review["starScore"],
                                           author=review["userId"],
                                           sentence_post_date=review["registerDate"],
                                           sentence_type="review")
                        except:
                            continue
                    page += 1
                        # item["selectedOption"]
        # else:
        #     self.db.update_one("crawl_contents", "crawl_status","ER", "contents_id", self.contents_id)
        #     return
        self.db.update_one("crawl_contents", "crawl_status", "GF", "contents_id", self.contents_id)



