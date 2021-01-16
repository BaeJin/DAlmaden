import sys
sys.path.append('../')
from engine.crawler.crawLibtwitter import CrawlLibTwitter

search_key = '송전탑'
channel = 'twitter'
startDate = '2020-11-01'
endDate = '2020-11-30'
nCrawl = 100

crawler = CrawlLibTwitter(search_key, channel, startDate, endDate,nCrawl)
crawler.crawl()

