# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from dacrawler.items import NavershoppingItem
from scrapy import Selector
from ..items import NavershoppingListItem

class NavershoppingListSpider(scrapy.Spider):
    name = 'navershopping'
    category = '헤어드라이어'
    allowed_domains = ['https://search.shopping.naver.com/']
    start_urls = ['https://search.shopping.naver.com//']
    browser = webdriver.Chrome('c:/chromewebdriver/chromedriver.exe')


    def start_requests(self):
        for i in range(1,5,1) : #pagenation
            yield scrapy.Request(f"https://search.shopping.naver.com/search/all?baseQuery={self.category}&frm=NVSHATC&pagingIndex={i}&pagingSize=40&productSet=total&query={self.category}&sort=rel&timestamp=&viewType=list", self.parse)

    def parse(self, response):
        self.browser.get(response.url)
        scrollHeight = 0
        last_scrollHeight = -1
        while scrollHeight != last_scrollHeight :
            eles = self.browser.find_elements_by_css_selector('.basicList_item__2XT81')
            for ele in eles :
                item = NavershoppingListItem()
                html = ele.get_attribute('outerHTML')
                selector = Selector(text=html)

                #scrapping
                item['category'] = self.category
                item['channel'] = self.name
                item['etc'] = selector.css('.basicList_img_area__a3NRA a img::attr(src)').extract()  #이미지 링크
                item['productName'] = selector.css('.basicList_title__3P9Q7 a::text').extract()
                item['maker'] = item['productName'].split[' '][0]
                item['price'] = selector.css('.price_num__2WUXn::text').extract()


                isThereReview = True if "리뷰" in " ".join(selector.css('.basicList_etc_box__1Jzg6 > a::text').extract()) else False
                if isThereReview :
                    item['url'] = selector.css('.basicList_etc_box__1Jzg6 > a::attr(href)').extract()

                item['nReview']
                item['nSold']
                item['options']

                item['updateDate']
            #scroll down
            self.browser.execute_script('arguments[0].scrollIntoView();', eles[-1])
            last_scrollHeight, scrollHeight = scrollHeight, self.browser.execute_script('return document.body.scrollHeight')
        # for row in response.css('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/div/div') :
        #     item = NavershoppingItem()
        #     item.productName = row.
