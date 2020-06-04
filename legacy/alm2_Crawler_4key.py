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



keyword1 = '사과'
keyword2 = '식초'
keyword3 = '냄새'
keyword4 = '우유'
keyword4 = '껍질'

channel = 'Naver Blog'

startDate = '2010-01-01'
endDate = '2019-12-31'





#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate, endDate)
crawler2 = NaverBlogCrawler(keyword2, channel, startDate, endDate)
crawler3 = NaverBlogCrawler(keyword3, channel, startDate, endDate)
crawler4 = NaverBlogCrawler(keyword4, channel, startDate, endDate)

th1 = Thread(target=crawler1.crawlUrlTexts)
th2 = Thread(target=crawler2.crawlUrlTexts)
th3 = Thread(target=crawler3.crawlUrlTexts)
th4 = Thread(target=crawler4.crawlUrlTexts)

th1.start()
th2.start()
th3.start()
th4.start()

th1.join()
th2.join()
th3.join()
th4.join()
