from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus_3keywords import *
import matplotlib.pyplot as plt

########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword1 = '스타일러'
keyword2 = '세탁기'
keyword3 = 'TV'

channel = 'Naver Blog'

startDate = '2011-01-01'
endDate = '2013-12-31'





#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate, endDate)
crawler2 = NaverBlogCrawler(keyword2, channel, startDate, endDate)
crawler3 = NaverBlogCrawler(keyword3, channel, startDate, endDate)

th1 = Thread(target=crawler1.crawlUrlTexts)
th2 = Thread(target=crawler2.crawlUrlTexts)
th3 = Thread(target=crawler3.crawlUrlTexts)
th1.start()
th2.start()
th3.start()
th1.join()
th2.join()
th3.join()
