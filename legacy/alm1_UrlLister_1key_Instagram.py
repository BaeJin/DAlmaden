from threading import Thread
from crawlLibInstagram import *


########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword1 = '마스크'

channel = 'Instagram'



nUrl = 9000


##### URL List 생성
# delete from urllist
# delete from htdocs

InstagramLister1=InstagramLister(nUrl, keyword1, channel)
InstagramLister1.getInstagramUrl()
