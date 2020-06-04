from threading import Thread
from crawlLibNaverBlog_12 import *
from crawlLibYouTube import *
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



keyword1 = '세븐나이츠'

channel = 'YouTube'

startDate = '2018-01-01'
endDate = '2020-02-28'

nUrl = 10000


##### URL List 생성
# delete from urllist
# delete from htdocs

yt1 = YouTubeCrawler('T0  ', channel)
yt1.openBrowser()
yt1.getVideoItems(keyword1, nUrl, startDate, endDate)
yt1.closeBrowser()


