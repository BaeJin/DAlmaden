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


channel = 'Naver Blog'

startDate1 = '2010-01-01'
endDate1 = '2014-12-31'

startDate2 = '2015-01-01'
endDate2 = '2019-12-31'





nUrl = 1000


##### URL List 생성
# delete from urllist
# delete from htdocs

urlLister1 = NaverBlogLister(nUrl, keyword1, channel, startDate1, endDate1)
urlLister2 = NaverBlogLister(nUrl, keyword1, channel, startDate2, endDate2)

urlLister1.createNaverBlogUrlList()
urlLister2.createNaverBlogUrlList()
# urlLister3.createNaverBlogUrlList()
