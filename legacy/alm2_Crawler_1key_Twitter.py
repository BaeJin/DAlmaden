from threading import Thread
from crawlLibTwitter import *

#########################################

keyword = '문재인'
channel = 'Twitter'




Twcrawler = TwitterCrawler(keyword, channel)
Twcrawler.crawlUrlTexts()
