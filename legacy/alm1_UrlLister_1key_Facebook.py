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



keyword1 = '코오롱 스포츠'

channel = 'Facebook'



nUrl = 1000


##### URL List 생성
# delete from urllist
# delete from htdocs

FacebookLister1=FacebookLister(nUrl, keyword1, channel)
FacebookLister1.getFacebookUrl()

