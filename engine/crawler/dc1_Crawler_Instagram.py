import sys
from pathlib import Path
from engine.crawler.crawlLibInstagram import CrawlLibInstagram


# username = 'kjyggg'
# password = 'xmrwodud01.'
keyword = '드라이기'

crawler = CrawlLibInstagram(keyword=keyword,get_nTotal=False)
crawler.start_requests()
# crawler = CrawlLibInstagram(task_id=1,keyword=keyword)
# crawler.crawl_total()
