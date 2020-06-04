from threading import Thread
from crawlLibNaverBlog import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt
import sys

########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword1 = sys.argv[1]

channel = 'Naver Blog'


startDate = '2015-01-01'
endDate = '2020-03-27'




#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate, endDate)


th1 = Thread(target=crawler1.crawlUrlTexts)
th1.start()
th1.join()

