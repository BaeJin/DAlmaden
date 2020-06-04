from threading import Thread
from crawlLibFacebook import *

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



nUrl = sys.argv[3]


##### URL List 생성
# delete from urllist
# delete from htdocs

FacebookLister1=FacebookLister(nUrl, keyword, channel)
FacebookLister1.getFacebookUrl()

