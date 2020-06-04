from crawlLibNaverBlog import *
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




keyword1 = sys.argv[1]


channel = sys.argv[2]


startDate = sys.argv[3]
endDate = sys.argv[4]

nUrl = int(sys.argv[5])


##### URL List 생성
# delete from urllist
# delete from htdocs

urlLister1 = NaverBlogLister(nUrl, keyword1, channel, startDate, endDate)


urlLister1.createNaverBlogUrlList()


