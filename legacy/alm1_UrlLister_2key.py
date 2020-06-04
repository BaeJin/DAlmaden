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


keyword1 = '출청남도 인구'
keyword2 = '충청남도 주택'
channel = 'Naver Blog'



stime = datetime.now()
startDate1 = '2014-01-01'
endDate1 = '2014-12-31'

startDate2 = '2014-01-01'
endDate2 = '2014-12-31'
nUrl = 4000


##### URL List 생성
# delete from urllist
# delete from htdocs

urlLister1 = NaverBlogLister(nUrl, keyword1, channel, startDate1, endDate1)
urlLister2 = NaverBlogLister(nUrl, keyword2, channel, startDate2, endDate2)

urlLister1.createNaverBlogUrlList()
urlLister2.createNaverBlogUrlList()

ftime = datetime.now()

Time_taken = ftime - stime
print(Time_taken)
