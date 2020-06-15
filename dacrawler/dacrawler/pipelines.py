# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exceptions import DropItem


class DacrawlerPipeline:
    def process_item(self, item, spider):
        return item

class NavershoppingListPipeline :
    def __init__(self):
        self.url_seen = set()
    def process_item(self, item, spider):
        url = ''.join(item['url'])
        if url in self.url_seen :
            raise DropItem("Duplicate item found: %s" % item)
        else :
            self.url_seen.add(url)
            etcInfo = ' '.join(item['etc'])
            item['nReview'] = 1 if '리뷰' in etcInfo else 0
            item['updateDate'] = re.sub("[^0-9]","",etcInfo)
            return item