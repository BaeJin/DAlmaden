from threading import Thread
from crawlLibTwitter import *


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
startDate = sys.argv[3]
endDate = sys.argv[4]

nUrl = 2000

TwitterLister = TwitterLister(nUrl, keyword, channel, startDate, endDate)
TwitterLister.getTwitterUrl()

