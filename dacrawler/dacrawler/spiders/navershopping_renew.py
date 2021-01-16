# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import Selector
from scrapy.http import FormRequest
import json
import time
import random
from bs4 import BeautifulSoup
import requests
from ..almaden import Sql
from ..items import ShoppingListItem
from ..items import ShoppingReviewItem
import re

CUSTOM_HEADER = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1v485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
    'referer': 'https://cr.shopping.naver.com/adcr.nhn?x=UqdHTJoNTCLmDRJmeUnHlf%2F%2F%2Fw%3D%3Dso9VDpccOJEJRAIk8kuUlxMWrABtahSEWMaqJo3m9UbdvL12W5aYi%2FTl6p%2B3d7gt2UDGZeWTm1v%2BM3dgb6pD%2BDcA8tPryz%2FlDyJRIn%2F3GbdYxTbKPi8joU3Nl4X0DXHSo3Y9fIdJ5zZ5Cp5gsTRBKAtyGaSr%2B0dRu37W7MMIB4NGtrk2YZNI7XPUxwzPc48d9mgXdPaip9zehn8GnNDvG2V9H67KEMncnWpoX4ZNWSLk4bc4NKsfCCJHgd8ZAW%2BSc%2FLKc3OGGtGoebD6lZ4I44ISv2w0Yv0stZD6LKftbf55bUf73NilrRL4RDYk4DmFeq3btKVxhUpidTfV6BgzPrJl5ZvLlNP%2B%2FvAE%2FR15kJfy9835OhANBmT1EtNrHhr2FCt5YK%2FmGsUxO25%2F2s6FZQcOmY27ZGze0Q%2BtXRlM4OxtarJoVrbEtunAYIkKGowOqukzgPDVXo6AvL8aV8tkrWSEhb%2B5%2BbgCLWD5ufmjwVaC0c1bmOP2u2YumOF3Sc7ORjT3CA11g7crAXPKtuqjMF6AhfbmRc6T9Q91MqoVII6q9tyiYebOu2HANWNhP0a1Sk4qXti8zVzVPIzmwp4FnMxjpTF8mUvzAqbc%2BYg0Db%2FqzD%2B13y5qA3088r1MNA5Dgw2popvk5HxytjbrmvguYxNgCgu8TH6IETI9IR%2BJIKXeXzoAYWtugk3VcH2L2xPlsYFx8Zt3N1gkRM4V7K6KABgau4fTwOUqyF63FjwpQRls%3D&nvMid={}&catId=50001986',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

CHANNEL = 'navershopping'
CATEGORY = '코딩'
#product
PRODUCT_MAX_PAGE = 1
#review
REVIEW_START_PRODUCT_ID = 0
REVIEW_START_PAGE = 1

class NavershoppingListSpider(scrapy.Spider):
    name = 'navershopping_product_kjy'
    channel = CHANNEL
    category = CATEGORY
    #allowed_domains = ['https://search.shopping.naver.com/']
    #start_urls = ['https://search.shopping.naver.com//']

    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.NavershoppingListPipeline": 1},
        'FEED_FORMAT' : "csv",
        'FEED_URI' : "navershoppinglist.csv"
    }
    page = 1
    MAX_PAGE = PRODUCT_MAX_PAGE

    def start_requests(self):
        self.browser = webdriver.Chrome('c:/chromewebdriver/chromedriver.exe')
        yield scrapy.Request(f"https://search.shopping.naver.com/search/all?baseQuery={self.category}&frm=NVSHATC&pagingIndex={self.page}&pagingSize=40&productSet=total&query={self.category}&sort=rel&timestamp=&viewType=list", self.parse)

    def parse(self, response):
        self.browser.get(response.url)
        scrollHeight = 0
        nScroll = 0
        MAXScroll = 3
        while nScroll<MAXScroll:
            print('nscroll : ', nScroll)
            time.sleep(1)
            eles = self.browser.find_elements_by_css_selector('.basicList_item__2XT81')
            print("length", len(eles))

            for i, ele in enumerate(eles) :
                item = ShoppingListItem()
                try :
                    print('getting html')
                    html = ele.get_attribute('outerHTML')
                except Exception as ex:
                    print(ex)
                    continue

                selector = Selector(text=html)
                #scrapping
                item['category'] = self.category
                item['channel'] = self.channel
                item['etc'] = selector.css('.basicList_img_area__a3NRA a img::attr(src)').extract()  #이미지 링크
                item['productName'] = selector.css('.basicList_title__3P9Q7 a::text').extract()
                item['price'] = selector.css('.price_num__2WUXn::text').extract()
                #item['nReview'] = selector.css('.basicList_graph__ZV6s9 basicList_num__1yXM9::text').extract()
                item['url'] = selector.css('.basicList_etc_box__1Jzg6 > a::attr(href)').extract()

                item['grouped_by_shop'] = selector.css('.basicList_compare__3AjuT')
                if len(item['grouped_by_shop'])> 0 :
                    item['grouped_by_shop'] = 'T'
                else:
                    item['grouped_by_shop'] = 'F'
                item['url'] = item['url'][0] if len(item['url'])>0 else None
                item['crawled'] = 'F'
                    # item['url'] = item['url'][0]
                #item['options'] = selector.css('.basicList_detail_box__3ta3h::text').extract()
                item['etc'] = selector.css('.basicList_etc__2uAYO::text').extract()
                print('item_info:',item)
                yield item

            #scroll down
            scrollPostion1 = self.browser.execute_script('return window.pageYOffset;')
            self.browser.execute_script('arguments[0].scrollIntoView();', eles[-1])
            scrollPostion2 = self.browser.execute_script('return window.pageYOffset;')
            print(scrollPostion1, scrollPostion2)
            if scrollPostion1 == scrollPostion2 :
                print("SCROLLLLLLLLLLLLLLLLLLLLL")
                self.browser.execute_script("window.scrollBy(0, +200);")
                #print(self.browser.execute_script('return window.pageYOffset;'))
            # time.sleep(1)
            last_scrollHeight = scrollHeight
            scrollHeight = self.browser.execute_script('return document.body.scrollHeight')
            if last_scrollHeight == scrollHeight :
                 nScroll += 1
            else :
                 nScroll = 0
        self.page+=1
        if self.page <= self.MAX_PAGE :
            print(self.page,"!!!!!"*100)
            yield scrapy.Request(f"https://search.shopping.naver.com/search/all?baseQuery={self.category}&frm=NVSHATC&pagingIndex={self.page}&pagingSize=40&productSet=total&query={self.category}&sort=rel&timestamp=&viewType=list", self.parse, dont_filter=True)
        else :
            self.browser.close()


class NavershoppingReviewSpider(scrapy.Spider):
    ## 경로 C:\Users\wodud\PycharmProjects\DAlmaden\dacrawler\dacrawler> scrapy crawl navershopping_review_test

    name = 'navershopping_review_kjy'
    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.NavershoppingReviewPipeline": 2},
    }

    url = 'https://search.shopping.naver.com/detail/review_list.nhn'
    formdata = {'nvMid':None, 'page':1, 'reviewSort':'accuracy', 'reviewType':'all','ligh':'true'}
    nvMid_dict = {}
    url_list = []
    grouped_by_shop_list = []
    db = Sql('salmaden', hostIP='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com'
             , port=3306 , userID='datacast', password='radioga12!')
    start_productID = REVIEW_START_PRODUCT_ID
    start_page = REVIEW_START_PAGE

    def start_requests(self):
        ids = self.db.select('product','id,url,site_productID,grouped_by_shop', f"channel = 'navershopping' and category= '{CATEGORY}' and crawled='F'")
        for id in ids:
            check_ad = id['url'].startswith('https://adcr.naver.com/adcr?')
            self.nvMid_dict[id['id']] = id['site_productID'] if not check_ad else 0
            self.url_list.append(id['url'])
            self.grouped_by_shop_list.append(id['grouped_by_shop'])

        yield scrapy.Request('http://daum.net', self.parse)

    def parse(self, response):
        retry=0
        for (product_id, nvMid),url,grouped_by_shop in zip(self.nvMid_dict.items(),self.url_list, self.grouped_by_shop_list) :
            self.formdata['nvMid']= nvMid
            print((product_id, nvMid),grouped_by_shop)
            CUSTOM_HEADER['referer'] = CUSTOM_HEADER['referer'].format(nvMid)
            if self.start_page > 1 :
                page = self.start_page
                self.start_page = 1
            else :
                page = 1
                ###navershopping 으로 넘어가는 경우 nvMid 의 번호가 2로 시작한다.
            if grouped_by_shop=='T':
                print('is is grouped by shop')
                while retry < 3:
                    print('navershopping', product_id, nvMid)
                    self.formdata['page'] = page
                    time.sleep(random.random() * 5)

                    res = requests.post(self.url, data=self.formdata, headers = CUSTOM_HEADER)
                    print(res.status_code)
                    if res.status_code == requests.codes.ok:
                        retry = 0
                        soup = BeautifulSoup(res.text,'html.parser')
                        reviews = soup.select(".atc_area")

                        if len(reviews) < 1 : break
                        for review in reviews :
                            selector = Selector(text=str(review.contents))
                            item = ShoppingReviewItem()
                            item["product_id"] = product_id
                            item["site_productId"] = nvMid
                            item["text"] = selector.css('div.atc::text').extract()
                            item["postInfo"] = selector.css('.info_cell::text').extract()
                            item["rating"] = selector.css('.curr_avg strong::text').extract()
                            item["rating"] = float(item["rating"][0]) if item["rating"] is not None else None
                            #item["selectedOption"]
                            print(item)
                            yield item
                        page+=1
                    else :
                        retry += 1

            elif grouped_by_shop=='F':
                origin_productNo = 0
                machandiseNo = ''
                try:
                    ###smartstore 제품군의 경우 번호가 1 ,8 ,9
                    ##custom_header 업데이트 시켜주기
                    print('smartstore')
                    print('smartstore', product_id, nvMid, url)
                    CUSTOM_HEADER['referer'] = 'https://smartstore.naver.com/'
                    ###1. 표시되는 url 을 통해서 referer url 찾아내기
                    ###표시되는 url 로 접근

                    ###리뷰page 의 referer url 을 가져오기 위해 해당 위치 데이터를 읽어온다.
                    res = requests.get(url, headers=CUSTOM_HEADER)
                    print(product_id,':','res.status_code:',res.status_code)
                    time.sleep(3)
                    htmlSource = res.text
                    soup = BeautifulSoup(htmlSource, 'lxml')

                    ##referer url 은 script 태그 안에 type 속성(속성값: application/ld+json) 에 들어있음.
                    page_info = soup.find('script', {'type': 'application/ld+json'})
                    print('page_info:',page_info)
                    ##original product no 가져오기
                    script_json = soup.find('script',text=re.compile("window.__PRELOADED_STATE__="))
                    origin_json = str(script_json)[str(script_json).find('window.__PRELOADED_STATE__='):str(script_json).find('module={}')]
                    origin_json = origin_json.replace("</script","")
                    origin_json = json.loads(origin_json.replace('window.__PRELOADED_STATE__=',''))
                    origin_productNo = origin_json['product']['A']['productNo']
                    machandiseNo = origin_json['smartStore']['channel']['payReferenceKey']
                    ##현재 referer url 가져오기 위한 작업 1. 태그 내의 text 를 json 으로 변환시키고 url 값만 가져온다.
                    page_info_text = str(page_info)
                    page_info_text = page_info_text.replace('<script data-react-helmet="true" type="application/ld+json">',"")
                    page_info_text = page_info_text.replace('</script>', "")
                    print('page_info_text:',page_info_text)
                    page_info_json = json.loads(page_info_text)

                    page_referer_url = page_info_json['offers']['url']
                    print('page_referer_url:',page_referer_url)

                except Exception as e:
                    print('wow_error_is:',e)
                    self.db.update('product', rowId=product_id, colname_id='id', crawled='E')
                    continue
                while retry < 10:

                    ## 2. referer url 을 이용해 page 의 review 긁어오기
                    # 가져온 referer url 을 이용해 cutom_header의 referer 속성값을 없데이트 시킨다.
                    CUSTOM_HEADER['referer'] = page_referer_url
                    if origin_productNo==0:
                        newProductNo = page_referer_url.split("/")[-1]
                    else:
                        newProductNo= origin_productNo
                    print(CUSTOM_HEADER['referer'])
                    # page number 를 업데이트 시킨다.
                    review_page_url = 'https://smartstore.naver.com/i/v1/reviews/paged-reviews?page={}&pageSize=20&merchantNo={}&originProductNo={}&sortType=REVIEW_RANKING'.\
                        format(page,machandiseNo,newProductNo)
                    print('review_page_url:',review_page_url)
                    try:
                        res = requests.get(review_page_url, headers=CUSTOM_HEADER)
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        print(res.status_code)
                        input()

                    ###review page 에 접근이 됐으면 아래 작업을 통해 리뷰 데이터를 추출한다.
                    if res.status_code == requests.codes.ok:
                        try:
                            res_json = res.json()
                            print(res_json)
                            reviews = res_json['contents']
                            print(reviews)
                        except:
                            retry+=1
                            continue
                        retry = 0
                        if len(reviews) < 1 : break
                        for review in reviews :
                            item = ShoppingReviewItem()
                            item["product_id"] = product_id
                            item["site_productId"] = nvMid
                            item["text"] = review["reviewContent"]
                            item["postInfo"] = None
                            item["rating"] = float(review['reviewScore'])
                            #item["selectedOption"]
                            yield item
                        page+=1
                    else :
                        retry += 1
                        time.sleep(3)
            if retry>=10:
                self.db.update('product',rowId= product_id,colname_id='id',crawled='E')
                retry=0
                print('{}:error'.format(product_id))
            else:
                print('{}:success'.format(product_id))
                self.db.update('product',rowId= product_id,colname_id='id',crawled='T')