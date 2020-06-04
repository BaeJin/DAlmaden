from threading import Thread
from crawlLibTwitter import *

#########################################

keyword = sys.argv[1]
channel = 'Twitter'



Twcrawler = TwitterCrawler(keyword, channel)
Twcrawler.crawlUrlTexts()
