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



keyword1 = 'Needle-Free Drug Delivery Devices'
keyword2 = 'kt 5g'

channel = 'Naver Blog'


startDate = '2018-01-01'
endDate = '2019-07-11'

nUrl = 50


##### URL List 생성
# delete from urllist
# delete from htdocs

urlLister1 = NaverBlogLister(nUrl, keyword1, channel, startDate, endDate)
urlLister2 = NaverBlogLister(nUrl, keyword2, channel, startDate, endDate)

urlLister1.createNaverBlogUrlList()
urlLister2.createNaverBlogUrlList()

