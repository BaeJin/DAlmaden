from threading import Thread
from crawlLibNaverBlog_12 import *
from crawlLibYouTube import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt
import pymysql

########################################################################################################################

##      ##        ##        ######    ##      ##
####  ####      ##  ##        ##      ##      ##
##  ##  ##    ##      ##      ##      ####    ##
##  ##  ##    ##      ##      ##      ##  ##  ##
##      ##    ##########      ##      ##    ####
##      ##    ##      ##      ##      ##      ##
##      ##    ##      ##    ######    ##      ##

########################################################################################################################


keyword1 = '코오롱 스포츠 김혜자'

channel = 'YouTube'

startDate = '1900-01-01'
endDate = '2999-12-31'

#### 생성된 URL List에 대해 crawling

yt1 = YouTubeCrawler('T0   ', channel)

ytVideoInfoList = yt1.readUrlListFromDB(keyword1)



nThread = 4
urlLists = []
ytContentList = []
ytCrawlers = []
for i in range(0, nThread):
    urlLists.append([])
    ytContentList.append([])
    ytc = YouTubeCrawler('T%d   ' % (i), channel)
    ytCrawlers.append(ytc)
    ytc.openBrowser()

idx = 0
for v in ytVideoInfoList:
    urlListNo = idx % nThread
    urlLists[urlListNo].append(v)
    idx += 1



th = []
for i in range(0, nThread):
    th.append(Thread(target=ytCrawlers[i].storeContentsIntoList, args=(urlLists[i], ytContentList[i])))

for i in range(0, nThread):
    th[i].start()

for i in range(0, nThread):
    th[i].join()

for i in range(0, nThread):
    print(
        "\n\n========================================================================================================\n\nAt List ",
        i)
    for ycItem in ytContentList[i]:
        print("\n\n<", ycItem.title[0:30], "> : nReply=", ycItem.nReply)
        print(ycItem.titleDesc[0:30])
        for c in ycItem.comments:
            print(">>", c.publishTime, c.text[0:30])

for i in range(0, nThread):
    ytCrawlers[i].writeDocsToDB(keyword1, channel, ytContentList[i])

for i in range(0, nThread):
    ytCrawlers[i].closeBrowser()




