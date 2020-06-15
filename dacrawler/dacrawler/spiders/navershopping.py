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
from ..items import NavershoppingListItem
from ..items import NavershoppingReviewItem

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
                item = NavershoppingListItem()
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

    def start_requests(self):
        ids = self.db.select('product','id, site_productID')
        for id in ids :
            if id['site_productID'] :
                self.nvMid_dict[id['id']] = id['site_productID']
        self.nvMid_dict = dict(sorted(self.nvMid_dict.items()))
        print(self.nvMid_dict)
        yield scrapy.Request('https://search.shopping.naver.com', self.parse)

    def parse(self, response):
        for product_id, nvMid in self.nvMid_dict.items() :
            print(product_id, nvMid)
            self.formdata['nvMid']= nvMid
            page = 0
            while True :
                page+=1
                print(page)
                self.formdata['page'] = page
                time.sleep(random.random() * 5)
                res = requests.post(self.url, data=self.formdata)
                if res.status_code == requests.codes.ok:
                    soup = BeautifulSoup(res.text,'html.parser')
                    reviews = soup.select(".atc_area")
                    if len(reviews) < 0 : break
                    for review in reviews :
                        selector = Selector(text=str(review.contents))
                        item = NavershoppingReviewItem()
                        item["product_id"] = product_id
                        item["site_productId"] = nvMid
                        item["text"] = selector.css('div.atc::text').extract()
                        item["postInfo"] = selector.css('.info_cell::text').extract()
                        item["rating"] = selector.css('.curr_avg strong::text').extract()
                        #item["selectedOption"]
                        yield item

