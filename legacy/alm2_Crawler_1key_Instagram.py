from threading import Thread
#from crawlLibNaverBlog import *
#from crawlLibYouTube import *
#from textAnalyzer import *
#from renderWordCloud import *
#from setCalculus import *
from crawlLibInstagram import * 
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



keyword1 = '전자담배'
channel = 'Instagram'






Itcrawler = InstagramCrawler(keyword1, channel)

Itcrawler.crawlUrlTexts()
