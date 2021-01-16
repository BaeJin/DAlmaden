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
    'authority': 'www.amazon.com',
    'cache-control': 'max-age=0',
    'rtt': '150',
    'downlink': '6.65',
    'ect': '4g',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'session-id=143-4184808-4175519; i18n-prefs=USD; sp-cdn=^\\^L5Z9:KR^\\^; ubid-main=131-3864953-3624011; lc-main=en_US; session-id-time=2082787201l; skin=noskin; session-token=uz+sSjctsGaz9Z0kfICd/5jj+MLUiJI1AAzdfKFGy9T6Zf0O2iNNEphijimeFK/A0HVsa6uS/YqRbUMslMprwn74seepAG3WHuC99IUr018zgf8MemEokh+HxcGX7T7RIA2vFUeIxDJpZSR9PD2uUhMdIbeq4pc8C4ipMndN0iVMpvrrHftyY1QSuyIAEWrl; csm-hit=adb:adblk_no^&t:1598336032599^&tb:2RBP3SA94EREVSD2TXNZ+s-2RBP3SA94EREVSD2TXNZ^|1598336032599',
}

CHANNEL = 'amazon'
CATEGORY = 'sleep aid device'
#product
PRODUCT_MAX_PAGE = 1
#review
REVIEW_START_PRODUCT_ID = 0
REVIEW_START_PAGE = 0

cate_url = CATEGORY.replace(" ","+")


class AmazonListSpider(scrapy.Spider):
    name = 'amazon_product'
    channel = CHANNEL
    category = CATEGORY
    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.AmazonListPipeline": 1},
        'FEED_FORMAT' : "csv",
        'FEED_URI' : "amazonlist.csv",
        'USER_AGENT' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }
    MAX_PAGE = PRODUCT_MAX_PAGE

    start_urls = [f"https://www.amazon.com/s?k={cate_url}&page={i}&qid=1592307818&ref=sr_pg_{i}" for i in range(1,MAX_PAGE+1)]
    print('start_urls:',start_urls)
    def parse(self, response):
        containers = response.css("div.a-section.a-spacing-medium")
        print('len(containers):',len(containers))
        for container in containers :
            item = ShoppingListItem()
            item['category'] = self.category
            item['channel'] = self.channel
            item['etc'] = container.css('div.a-section.aok-relative.s-image-square-aspect img::attr(src)').extract()  # 이미지 링크
            item['productName'] = container.css('span.a-color-base.a-text-normal::text').extract()
            item['price'] = container.css('a.a-size-base.a-link-normal.a-text-normal>span.a-price>.a-offscreen::text').extract()
            item['nReview'] = container.css('div.a-row.a-size-small a.a-link-normal .a-size-base::text').extract()
            item['url'] = container.css('div.a-row.a-size-small a.a-link-normal::attr(href)').extract()
            if len(item['url'])==0:
                continue
            print("item_info:",item)
            yield item

class AmazonReviewSpider(scrapy.Spider):
    name = 'amazon_review'
    channel = CHANNEL
    category = CATEGORY

    custom_settings = {
        'ITEM_PIPELINES' : {"dacrawler.pipelines.AmazonReviewPipeline": 1},
        'USER_AGENT' : "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }
    db = Sql('salmaden', hostIP='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
             port=3306 , userID='datacast', password='radioga12!')
    products = {}
    start_productID = REVIEW_START_PRODUCT_ID
    start_page = REVIEW_START_PAGE

    def start_requests(self):
        products = self.db.select('product','id, url', f"channel = 'amazon' and category= '{CATEGORY}'")
        for product in products:
            if not product['url'] : continue
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