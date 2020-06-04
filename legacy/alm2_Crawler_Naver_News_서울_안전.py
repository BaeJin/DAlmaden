from crawlLibNaverNews import *
from threading import Thread
from datetime import datetime
import sys

keyword = "연수구 안전"
channel = "Naver Blog"
startDate = "2010-01-01"

endDate = "2014-12-31"
s_page = "1"
maxpage = "500"
crawler1 = NaverNewsLister(int(s_page), int(maxpage) , keyword, channel, startDate, endDate)
#crawler2 = NaverNewsLister(round((s_page+maxpage)/2), maxpage/2+1, keyword, channel, startDate, endDate)

crawler1.crawler()
#th2 = Thread(target=crawler2.crawler())

end = datetime.now()
