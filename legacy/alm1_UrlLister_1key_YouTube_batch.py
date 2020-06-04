from threading import Thread
from crawlLibNaverBlog_12 import *
from crawlLibYouTube import *
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



keyword1 = sys.argv[1]

channel = sys.argv[2]

startDate = sys.argv[3]
endDate = sys.argv[4]

nUrl = int(sys.argv[5])


##### URL List 생성
# delete from urllist
# delete from htdocs

yt1 = YouTubeCrawler('T0  ', channel)
yt1.openBrowser()
yt1.getVideoItems(keyword1, nUrl, startDate, endDate)
yt1.closeBrowser()


