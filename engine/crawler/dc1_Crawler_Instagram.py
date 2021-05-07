import sys
from pathlib import Path
from engine.crawler.crawlLibInstagram import CrawlLibInstagram


# username = 'kjyggg'
# password = 'xmrwodud01.'
keyword = '캠핑 음식'
crawler = CrawlLibInstagram(task_id=43412,keyword=keyword)
crawler.start_requests()
