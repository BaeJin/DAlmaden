import sys
sys.path.append('../')
from engine.crawler.crawlLibAmazon import CrawlLibAmazon



crawl_obj = CrawlLibAmazon(1,keyword='드라이기')
crawl_obj.crawl_total()
