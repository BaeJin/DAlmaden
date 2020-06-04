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

keyword1 = '등산복'
channel = 'Instagram'




Itcrawler = InstagramCrawler(keyword1, channel)

Itcrawler.crawlUrlTexts()