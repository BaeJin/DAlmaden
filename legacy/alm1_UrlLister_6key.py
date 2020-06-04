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



keyword1 = '반려동물'
keyword2 = '자녀양육'
keyword3 = '반려견'
keyword4 = '반려묘'
keyword5 = '애완동물'
keyword6 = '반려동물'

channel = 'Naver Blog'



startDate = '2010-01-01'
endDate = '2019-12-31'

nUrl = 2000


##### URL List 생성
# delete from urllist
# delete from htdocs

urlLister1 = NaverBlogLister(nUrl, keyword1, channel, startDate, endDate)
urlLister2 = NaverBlogLister(nUrl, keyword2, channel, startDate, endDate)
urlLister3 = NaverBlogLister(nUrl, keyword3, channel, startDate, endDate)
urlLister4 = NaverBlogLister(nUrl, keyword4, channel, startDate, endDate)
urlLister5 = NaverBlogLister(nUrl, keyword5, channel, startDate, endDate)
urlLister6 = NaverBlogLister(nUrl, keyword6, channel, startDate, endDate)



th1 = Thread(target=urlLister1.createNaverBlogUrlList())
th2 = Thread(target=urlLister2.createNaverBlogUrlList())
th3 = Thread(target=urlLister3.createNaverBlogUrlList())
th4 = Thread(target=urlLister4.createNaverBlogUrlList())
th5 = Thread(target=urlLister5.createNaverBlogUrlList())
th6 = Thread(target=urlLister6.createNaverBlogUrlList())

th1.start()
th2.start()
th3.start()
th4.start()
th5.start()
th6.start()

th1.join()
th2.join()
th3.join()
th4.join()
th5.join()
th6.join()