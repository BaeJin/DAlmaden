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
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cookie': 'session-id=144-6822887-3263134; ubid-main=134-0994494-1365267; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjB9; aws_lang=ko; aws-target-static-id=1591866605052-162145; aws-target-data=%7B%22support%22%3A%221%22%7D; s_fid=6C912779CF383042-1F8A239025F42F80; regStatus=pre-register; s_cc=true; aws-target-visitor-id=1591866605055-265359.32_0; s_dslv=1591940731932; s_vn=1623402605501%26vn%3D2; s_nr=1591940731937-Repeat; skin=noskin; session-id-time=2082787201l; i18n-prefs=USD; x-wl-uid=1lJ0DfuwJy/bExt9gBu/wxmJOG1huLJ7vP/Z7Yi1pet5JK3/BPZllNZcMLZnHdIR4+KX/urrZzB4=; session-token=SsEprkcfNePkTrLTST1OXl9NSxPTcQ3Xpk4Ak4vyyS+1XVlCHUpA3ctQogB57+w6tXWAceiiMlTqn9oGBC63Q5/5dCsEnI9ubQelH71m3zNTJxpqaKai/j8cGIlEmXKtuGDOBSY8y4V+lXmGD3S3OawfECksubb5NYHqkLv02ZxdQLSg4QiERXJLSJ859ve5; csm-hit=tb:FERFSTQ98644C9Y41Z5H+s-FERFSTQ98644C9Y41Z5H|1592307645170&t:1592307645170&adb:adblk_no',
    'referer': 'https://www.amazon.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}



class AmazonListSpider(scrapy.Spider):
    name = 'amazonlist'
    category = 'hair dryer'
    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.AmazonListPipeline": 1},
        'FEED_FORMAT' : "csv",
        'FEED_URI' : "amazonlist.csv",
        'USER_AGENT' : "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }
    MAX_PAGE = 7
    start_urls = ["https://www.amazon.com/s?k=hair+dryer&page={}&qid=1592307818&ref=sr_pg_{}".format(i,i) for i in range(1,MAX_PAGE+1)]

    def parse(self, response):
        time.sleep(3)
        containers = response.css("div.a-section.a-spacing-medium")
        for container in containers :
            item = ShoppingListItem()
            item['category'] = self.category
            item['channel'] = self.name
            item['etc'] = container.css('div.a-section.aok-relative.s-image-square-aspect img::attr(src)').extract()  # 이미지 링크
            item['productName'] = container.css('span.a-size-base-plus.a-color-base.a-text-normal::text').extract()
            item['price'] = container.css('a.a-size-base.a-link-normal.a-text-normal>span.a-price>.a-offscreen::text').extract()
            item['nReview'] = container.css('div.a-row.a-size-small a.a-link-normal .a-size-base::text').extract()
            item['url'] = container.css('div.a-row.a-size-small a.a-link-normal::attr(href)').extract()
            yield item

class AmazonReviewSpider(scrapy.Spider):
    name = 'amazonreview'
    category = 'hair dryer'

    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.AmazonReviewPipeline": 1},
        'USER_AGENT' : "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }
    db = Sql('salmaden')
    products = {}
    crawling_index = 0
    start_productID = 0
    start_page = 1

    def start_requests(self):
        for product in self.db.select('product', 'id, url', "channel = 'amazonlist'"):
            purl = product['url'].split("/")[1:-1]
            if not 'gp' in purl and product['id'] >= self.start_productID:
                purl[1] = 'product-reviews'
                purl = "/".join(purl)
                product_url = 'https://www.amazon.com/' + purl + '?ie=UTF8&reviewerType=all_reviews&pageNumber={}'
                self.products[product['id']] = product_url
            self.products = dict(sorted(self.products.items()))
        yield scrapy.Request('http://daum.net', self.parse)

    def parse(self, response):
        for id, url in self.products.items() :
            if self.start_page > 1 :
                page = self.start_page
                self.start_page = 1
            else :
                page = 1
            retry = 0
            while retry<3 :
                time.sleep(random.random() * 5)
                url_page = url.format(page)
                print(page, url_page)
                res = requests.get(url_page, headers = CUSTOM_HEADER)
                if res.status_code == requests.codes.ok:
                    retry = 0
                    soup = BeautifulSoup(res.text,'lxml')
                    reviews = soup.select(".a-section.review.aok-relative")
                    if len(reviews) < 1 : break
                    for review in reviews :
                        selector = Selector(text=str(review.contents))
                        item = ShoppingReviewItem()
                        item["product_id"] = id
                        item["site_productId"] = url_page
                        item["postInfo"] = selector.css('.review-date::text').extract()
                        item["rating"] = selector.css('.a-icon-alt::text').extract()
                        text = review.select_one('div.a-row.a-spacing-small.review-data > span').text
                        title = review.select_one('a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold > span').text
                        item["text"] = title+" :: "+text
                        yield item
                    page += 1
                else :
                    retry += 1



