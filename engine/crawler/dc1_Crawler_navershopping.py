import sys
sys.path.append('../')
from engine.crawler.crawlLibnavershopping_old import CrawlLibNavershopping
from datetime import datetime
import time


keyword='식사대용'
obj_nvs =CrawlLibNavershopping(task_id=10021,keyword=keyword)
# obj_nvs.crawl_total()
###키워드에 해당하는 product list 정보 가져오기 (list type)
# obj_nvs.crawl()
res = obj_nvs.get_product_info_by_api()
obj_nvs.crawl_total_review_count(res)

