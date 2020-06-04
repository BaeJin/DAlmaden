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



keyword1 = '삼성'
keyword2 = 'LG'
keyword3 = '애플'

channel = 'Naver Blog'

startDate = '2018-01-01'
endDate = '2019-07-01'

nUrl = 1000


##### URL List 생성
# delete from urllist
# delete from htdocs

urlLister1 = NaverBlogLister(nUrl, keyword1, channel, startDate, endDate)
urlLister2 = NaverBlogLister(nUrl, keyword2, channel, startDate, endDate)
urlLister3 = NaverBlogLister(nUrl, keyword3, channel, startDate, endDate)

urlLister1.createNaverBlogUrlList()
urlLister2.createNaverBlogUrlList()
urlLister3.createNaverBlogUrlList()
