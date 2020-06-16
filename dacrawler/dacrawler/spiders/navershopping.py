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


CUSTOM_HEADER = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
    'referer': 'https://cr.shopping.naver.com/adcr.nhn?x=UqdHTJoNTCLmDRJmeUnHlf%2F%2F%2Fw%3D%3Dso9VDpccOJEJRAIk8kuUlxMWrABtahSEWMaqJo3m9UbdvL12W5aYi%2FTl6p%2B3d7gt2UDGZeWTm1v%2BM3dgb6pD%2BDcA8tPryz%2FlDyJRIn%2F3GbdYxTbKPi8joU3Nl4X0DXHSo3Y9fIdJ5zZ5Cp5gsTRBKAtyGaSr%2B0dRu37W7MMIB4NGtrk2YZNI7XPUxwzPc48d9mgXdPaip9zehn8GnNDvG2V9H67KEMncnWpoX4ZNWSLk4bc4NKsfCCJHgd8ZAW%2BSc%2FLKc3OGGtGoebD6lZ4I44ISv2w0Yv0stZD6LKftbf55bUf73NilrRL4RDYk4DmFeq3btKVxhUpidTfV6BgzPrJl5ZvLlNP%2B%2FvAE%2FR15kJfy9835OhANBmT1EtNrHhr2FCt5YK%2FmGsUxO25%2F2s6FZQcOmY27ZGze0Q%2BtXRlM4OxtarJoVrbEtunAYIkKGowOqukzgPDVXo6AvL8aV8tkrWSEhb%2B5%2BbgCLWD5ufmjwVaC0c1bmOP2u2YumOF3Sc7ORjT3CA11g7crAXPKtuqjMF6AhfbmRc6T9Q91MqoVII6q9tyiYebOu2HANWNhP0a1Sk4qXti8zVzVPIzmwp4FnMxjpTF8mUvzAqbc%2BYg0Db%2FqzD%2B13y5qA3088r1MNA5Dgw2popvk5HxytjbrmvguYxNgCgu8TH6IETI9IR%2BJIKXeXzoAYWtugk3VcH2L2xPlsYFx8Zt3N1gkRM4V7K6KABgau4fTwOUqyF63FjwpQRls%3D&nvMid={}&catId=50001986',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}



class NavershoppingListSpider(scrapy.Spider):
    name = 'navershoppinglist'
    category = '헤어드라이어'
    #allowed_domains = ['https://search.shopping.naver.com/']
    #start_urls = ['https://search.shopping.naver.com//']

    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.NavershoppingListPipeline": 1},
        'FEED_FORMAT' : "csv",
        'FEED_URI' : "navershoppinglist.csv"
    }
    page = 1
    MAX_PAGE = 10

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
                item['channel'] = self.name
                item['etc'] = selector.css('.basicList_img_area__a3NRA a img::attr(src)').extract()  #이미지 링크
                item['productName'] = selector.css('.basicList_title__3P9Q7 a::text').extract()
                item['price'] = selector.css('.price_num__2WUXn::text').extract()
                #item['nReview'] = selector.css('.basicList_graph__ZV6s9 basicList_num__1yXM9::text').extract()
                item['url'] = selector.css('.basicList_etc_box__1Jzg6 > a::attr(href)').extract()
                #item['options'] = selector.css('.basicList_detail_box__3ta3h::text').extract()
                item['etc'] = selector.css('.basicList_etc__2uAYO::text').extract()
                yield item

            #scroll down
            scrollPostion1 = self.browser.execute_script('return window.pageYOffset;')
            self.browser.execute_script('arguments[0].scrollIntoView();', eles[-1])
            scrollPostion2 = self.browser.execute_script('return window.pageYOffset;')
            print(scrollPostion1, scrollPostion2)
            if scrollPostion1 == scrollPostion2 :
                print("SCROLLLLLLLLLLLLLLLLLLLLL")
                self.browser.execute_script("window.scrollBy(0, +200);")
                print(self.browser.execute_script('return window.pageYOffset;'))
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
    name = 'navershoppingreview'
    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.NavershoppingReviewPipeline": 2},
    }
    url = 'https://search.shopping.naver.com/detail/review_list.nhn'
    formdata = {'nvMid':None, 'page':1, 'reviewSort':'accuracy', 'reviewType':'all','ligh':'true'}
    nvMid_dict = {}
    db = Sql('salmaden')
    temp = True
    def start_requests(self):
        ids = self.db.select('product','id, site_productID')
        for id in ids :
            if id['site_productID'] :
                self.nvMid_dict[id['id']] = id['site_productID']
        startIndex = 3                                                                    #setting startindex
        self.nvMid_dict = dict(sorted(self.nvMid_dict.items())[startIndex:])
        print(self.nvMid_dict)
        yield scrapy.Request('http://daum.net', self.parse)

    def parse(self, response):
        for product_id, nvMid in self.nvMid_dict.items() :
            print(product_id, nvMid)
            self.formdata['nvMid']= nvMid
            CUSTOM_HEADER['referer'] = CUSTOM_HEADER['referer'].format(nvMid)
            if self.temp : page = 0                                                     #setting start page
            else : page, self.temp = 0, False
            retry = 0
            while retry<3 :
                page+=1
                print(page)
                self.formdata['page'] = page
                time.sleep(random.random() * 5)
                res = requests.post(self.url, data=self.formdata, headers = CUSTOM_HEADER)
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
                        #item["selectedOption"]
                        yield item
                else :
                    retry += 1
