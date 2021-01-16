# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exceptions import DropItem
from .almaden import Sql


class DacrawlerPipeline:
    def process_item(self, item, spider):
        return item

class NavershoppingListPipeline :
    def __init__(self):
        self.url_seen = set()
        self.db = Sql('salmaden', hostIP='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                      port=3306, userID='datacast', password='radioga12!')

    def process_item(self, item, spider):
        url = ''.join(item['url'])
        if url in self.url_seen :
            raise DropItem("Duplicate item found: %s" % item)
        if url.startswith('https://adcr.naver.com/adcr'):
            raise DropItem("Drop ad")
        else :
            self.url_seen.add(url)
            etcInfo = ' '.join(item['etc'])
            item['nReview'] = 1 if '리뷰' in etcInfo else 0
            item['updateDate'] = re.sub("[^0-9]","",etcInfo)
            try :
                item['price'] = int(re.sub('\D','',''.join(item['price'])))
            except :
                item['price'] = 0
            try :
                item['site_productID'] = re.sub(r"\D","",re.search(r'nvMid=\d+', ''.join(item['url'])).group())
            except :
                pass


            self.save_item(item)
            return item

    def save_item(self, item):
        try :
            item['etc'] = str(item['etc'])
            self.db.insert('product',**item)
        except Exception as ex :
            print(item)
            print(ex)

class NavershoppingReviewPipeline :
    def __init__(self):
        self.url_seen = set()
        self.db = Sql('salmaden', hostIP='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                      port=3306, userID='datacast', password='radioga12!')

    def process_item(self, item, spider):
        item['text'] = self.cleanse(' '.join([t.strip() for t in item['text']])) if type(item['text'])==list else re.sub(u"[^\x20-\x7E가-힣]", " ", item['text'])
        item["postInfo"] = str(item["postInfo"])
        self.save_item(item)
        return item

    def save_item(self, item):
        try :
            self.db.insert('review',**item)
        except Exception as ex :
            print(item)
            print(ex)
    def cleanse(self, text):
        # DB 저장을 위한 최소한의 클린징
        text = re.sub(u"[^\x20-\x7E가-힣]", " ", text)
        text = re.sub(u"\\s+", " ", text)
        return text.strip()


class AmazonListPipeline :
    def __init__(self):
        self.url_seen = set()
        self.db = Sql('salmaden', hostIP='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                      port=3306, userID='datacast', password='radioga12!')
    def process_item(self, item, spider):
        productInfo = [t.strip() for t in " ".join(item['productName']).split(",")]
        item['options'] = None
        try:
            item['price'] = re.sub("\D","",item['price'][0])
            item['nReview'] = item['nReview'][0]
            item['productName'] = item['productName'][0]
        except:
            print("item_info:",item)
            item['price'] = None
            item['nReview'] = None
            item['productName'] = None
        item['url'] = item['url'][0] if type(item['url']) is list and len(item['url'])>0 else item['url']
        self.save_item(item)
        return item

    def save_item(self, item):
        try :
            for k, v in item.items() :
                if type(v) is list and len(v) > 1 :
                    item[k] = str(v)
                else :
                    print(k, v)
            self.db.insert_withoutDuplication('product',['productName'],**item)
            print("insert_success")
        except Exception as ex :
            print('insert_error')
            print(ex)


class AmazonReviewPipeline :
    def __init__(self):
        self.url_seen = set()
        self.db = Sql('salmaden', hostIP='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                      port=3306, userID='datacast', password='radioga12!')

    def process_item(self, item, spider):
        item['text'] = self.cleanse(item['text'])
        item["postInfo"] = str(item["postInfo"])
        item['rating'] = float(' '.join(item['rating']).split(' ')[0])
        self.save_item(item)
        return item

    def save_item(self, item):
        try :
            self.db.insert('review',**item)
        except Exception as ex :
            print(ex)

    def cleanse(self, text):
        # DB 저장을 위한 최소한의 클린징
        text = re.sub(u"[^\x20-\x7E가-힣]", " ", text)
        text = re.sub(u"\\s+", " ", text)
        return text.strip()