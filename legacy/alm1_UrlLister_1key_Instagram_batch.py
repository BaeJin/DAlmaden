from threading import Thread
from crawlLibInstagram import *
#from textAnalyzer import *
#from renderWordCloud import *
#from setCalculus import *
#import matplotlib.pyplot as plt

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



nUrl = int(sys.argv[3])


##### URL List 생성
# delete from urllist
# delete from htdocs

InstagramLister1=InstagramLister(nUrl, keyword1, channel)
InstagramLister1.getInstagramUrl()
