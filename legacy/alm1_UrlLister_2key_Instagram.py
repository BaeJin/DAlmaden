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



keyword1 = '곶자왈'
keyword2 = '숲'

channel = 'Instagram'



nUrl = 600


##### URL List 생성
# delete from urllist
# delete from htdocs

InstagramLister1=InstagramLister(nUrl, keyword1, channel)
InstagramLister2=InstagramLister(nUrl, keyword1, channel)

InstagramLister1.getInstagramUrl()
InstagramLister2.getInstagramUrl()