from threading import Thread
from crawlLibNaverBlog import *
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



sstime = datetime.now()
keyword1 = '마스크'


channel = 'Naver Blog'

startDate1 = '2015-01-01'
endDate1 = '2015-12-31'
nUrl = 10000


##### URL List 생성
# delete from urllist
# delete from htdocs

urlLister1 = NaverBlogLister(nUrl, keyword1, channel, startDate1, endDate1)


urlLister1.createNaverBlogUrlList()



fftime= datetime.now() - sstime

print('fftime=',fftime)
