# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DacrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NavershoppingListItem(scrapy.Item) :
    channel = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    productName = scrapy.Field()
    price = scrapy.Field()
    maker = scrapy.Field()
    updateDate = scrapy.Field()
    nReview = scrapy.Field()
    nSold = scrapy.Field()
    nReview = scrapy.Field()
    options = scrapy.Field()
    etc = scrapy.Field()
    site_productID = scrapy.Field()

class NavershoppingRevieItem(scrapy.Item) :
    product_id = scrapy.Field()
    rating = scrapy.Field()
    text = scrapy.Field()
    selectedOption = scrapy.Field()
    postDate = scrapy.Field()

