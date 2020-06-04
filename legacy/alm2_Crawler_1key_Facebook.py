from threading import Thread
from crawlLibFacebook import * 
import matplotlib.pyplot as plt
import pymysql
import sys
########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword = sys.argv[1]
channel = sys.argv[2]






Facebookcrawler = FacebookCrawler(keyword, channel)

Facebookcrawler.crawlUrlTexts()

