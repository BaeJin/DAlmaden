# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import Selector
import time

from ..items import NavershoppingListItem

class NavershoppingListSpider(scrapy.Spider):
    name = 'navershopping'
    category = '헤어드라이어'
    allowed_domains = ['https://search.shopping.naver.com/']
    start_urls = ['https://search.shopping.naver.com//']
    browser = webdriver.Chrome('c:/chromewebdriver/chromedriver.exe')


    def start_requests(self):
        for i in range(1,3,1) : #pagenation
            yield scrapy.Request(f"https://search.shopping.naver.com/search/all?baseQuery={self.category}&frm=NVSHATC&pagingIndex={i}&pagingSize=40&productSet=total&query={self.category}&sort=rel&timestamp=&viewType=list", self.parse)

    def parse(self, response):
        self.browser.get(response.url)

        scrollHeight = 0
        last_scrollHeight = -1
        nScroll = 0
        MAXScroll = 3
        while nScroll<MAXScroll:
            print(scrollHeight, last_scrollHeight, nScroll)
            time.sleep(1)
            eles = self.browser.find_elements_by_css_selector('.basicList_item__2XT81')
            print("len elelssdfalksdfjasl;dfkjasdlfasjdlk", len(eles))

            for i, ele in enumerate(eles) :
                input(i)
                item = NavershoppingListItem()
                html = ele.get_attribute('outerHTML')
                selector = Selector(text=html)

                #scrapping
                item['category'] = self.category
                item['channel'] = self.name
                item['etc'] = selector.css('.basicList_img_area__a3NRA a img::attr(src)').extract()  #이미지 링크
                item['productName'] = selector.css('.basicList_title__3P9Q7 a::text').extract()
                item['price'] = selector.css('.price_num__2WUXn::text').extract()
                item['nReview'] = selector.css('.basicList_graph__ZV6s9 basicList_num__1yXM9::text').extract()
                item['url'] = selector.css('.basicList_etc_box__1Jzg6 > a::attr(href)').extract()
                item['options'] = selector.css('.basicList_detail_box__3ta3h::text').extract()
                item['updateDate'] = selector.css('.basicList_etc__2uAYO::text').extract()

                yield item

            #scroll down
            scrollPostion1 = self.browser.execute_script('return window.pageYOffset;')
            self.browser.execute_script('arguments[0].scrollIntoView();', eles[-1])
            scrollPostion2 = self.browser.execute_script('return window.pageYOffset;')
            print(scrollPostion1, scrollPostion2)
            if scrollPostion1 == scrollPostion2 :
                print("SCROLLLLLLLLLLLLLLLLLLLLL")
                self.browser.execute_script("window.scrollBy(0, 100);")
                nScroll+=1
                print(self.browser.execute_script('return window.pageYOffset;'))
            else :
                nScroll=0
            # time.sleep(1)
            input()
            # last_scrollHeight = scrollHeight
            # scrollHeight = self.browser.execute_script('return document.body.scrollHeight')
            # if last_scrollHeight == scrollHeight :
            #     nScroll += 1
            # else :
            #     nScroll = 0
            # print(last_scrollHeight, scrollHeight)
        # for row in response.css('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/div/div') :
        #     item = NavershoppingItem()
        #     item.productName = row.
