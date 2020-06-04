from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt
from datetime import datetime
########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################


keyword1 = '충청남도 인구'
keyword2 = '충청남도 주택'
channel = 'Naver Blog'



startDate = '2017-01-01'
endDate = '2017-12-31'

nUrl = 4000


#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate, endDate)
crawler2 = NaverBlogCrawler(keyword2, channel, startDate, endDate)

stime = datetime.now()
th1 = Thread(target=crawler1.crawlUrlTexts)
th2 = Thread(target=crawler2.crawlUrlTexts)
th1.start()
th2.start()
th1.join()
th2.join()
ftime = datetime.now()

Time_taken = ftime - stime

print(Time_taken)
