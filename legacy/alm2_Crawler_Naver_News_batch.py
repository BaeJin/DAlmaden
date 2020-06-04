from crawlLibNaverNews import *
from threading import Thread
from datetime import datetime
import sys

keyword = sys.argv[1]

channel = sys.argv[2]
startDate = sys.argv[3]

endDate = sys.argv[4]
s_page = sys.argv[5]
maxpage = sys.argv[6]

crawler1 = NaverNewsLister(int(s_page), int(maxpage) , keyword, channel, startDate, endDate)
#crawler2 = NaverNewsLister(round((s_page+maxpage)/2), maxpage/2+1, keyword, channel, startDate, endDate)

crawler1.crawler()
#th2 = Thread(target=crawler2.crawler())

end = datetime.now()
