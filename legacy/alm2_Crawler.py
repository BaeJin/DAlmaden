from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
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



keyword1 = '체리쉬 모션베드'
keyword2 = '한샘 모션베드'

channel = 'Naver Blog'

startDate = '2017-01-01'
endDate = '2019-12-31'





#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate, endDate)
crawler2 = NaverBlogCrawler(keyword2, channel, startDate, endDate)

th1 = Thread(target=crawler1.crawlUrlTexts)
th2 = Thread(target=crawler2.crawlUrlTexts)
th1.start()
th2.start()
th1.join()
th2.join()
