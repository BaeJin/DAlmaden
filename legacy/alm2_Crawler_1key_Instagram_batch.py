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



keyword1 = sys.argv[1]
channel = sys.argv[2]






Itcrawler = InstagramCrawler(keyword1, channel)
Itcrawler.crawlUrlTexts()
