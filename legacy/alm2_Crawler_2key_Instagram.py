from threading import Thread
#from crawlLibNaverBlog import *
#from crawlLibYouTube import *
#from textAnalyzer import *
#from renderWordCloud import *
#from setCalculus import *
from crawlLibInstagram import * 
import matplotlib.pyplot as plt
import pymysql
from threading import Thread

########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword1 = '곶자왈'
keyword2 = '숲'
channel = 'Instagram'






Itcrawler1 = InstagramCrawler(keyword1, channel)
Itcrawler2 = InstagramCrawler(keyword2, channel)


th1 = Thread(target = Itcrawler1.crawlUrlTexts())
th2 = Thread(target = Itcrawler2.crawlUrlTexts())

th1.start()
th2.start()
th1.join()
th2.join()