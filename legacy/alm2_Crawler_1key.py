from threading import Thread
from crawlLibNaverBlog import *
#from textAnalyzer import *
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


sstime = datetime.now()
keyword1 = '신제품'

channel = 'Naver Blog'


startDate1 = '2019-01-01'
endDate1 = '2020-04-27'


########################################################################################################################







#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate1, endDate1)


th1 = Thread(target=crawler1.crawlUrlTexts)

th1.start()

th1.join()

fftime= datetime.now() - sstime

print('fftime=',fftime)
