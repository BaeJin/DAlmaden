import sys
from pathlib import Path
from engine.crawler.crawLibtwitter import CrawlLibTwitter
import time

year_list = ['2016','2017','2018','2019','2020']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
date = ['31','28','31','30','31','30', '31', '31', '30', '31', '30', '31']
search_key = '송전탑'
channel = 'twitter'
nCrawl = 100

for year in year_list:
    for index, month in enumerate(month_list):
        start_date = '{}-{}-01'.format(year,month)
        end_date = '{}-{}-{}'.format(year,month,date[index])
        crawler = CrawlLibTwitter(search_key, channel, start_date,end_date,nCrawl)
        crawler.crawl()
