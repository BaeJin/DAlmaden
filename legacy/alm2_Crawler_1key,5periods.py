from threading import Thread
from crawlLibNaverBlog_12 import *
#from textAnalyzer import *
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



keyword1 = '서울 여성 일자리'


channel = 'Naver Blog'

startDate1 = '2015-01-01'
endDate1 = '2015-12-31'

startDate2 = '2016-01-01'
endDate2 = '2016-12-31'

startDate3 = '2017-01-01'
endDate3 = '2017-12-31'

startDate4 = '2018-01-01'
endDate4 = '2018-12-31'

startDate5 = '2019-01-01'
endDate5 = '2019-12-31'



#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate1, endDate1)
crawler2 = NaverBlogCrawler(keyword1, channel, startDate2, endDate2)
crawler3 = NaverBlogCrawler(keyword1, channel, startDate3, endDate3)
crawler4 = NaverBlogCrawler(keyword1, channel, startDate4, endDate4)
crawler5 = NaverBlogCrawler(keyword1, channel, startDate5, endDate5)

th1 = Thread(target=crawler1.crawlUrlTexts)
th2 = Thread(target=crawler2.crawlUrlTexts)
th3 = Thread(target=crawler3.crawlUrlTexts)
th4 = Thread(target=crawler4.crawlUrlTexts)
th5 = Thread(target=crawler5.crawlUrlTexts)

th1.start()
th2.start()
th3.start()
th4.start()
th5.start()

th1.join()
th2.join()
th3.join()
th4.join()
th5.join()
