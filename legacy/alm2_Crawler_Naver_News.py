from crawlLibNaverNews import *
from threading import Thread
from datetime import datetime
keyword = '서울시 공공임대 주택'

channel = 'Naver News'

startDate = '2018.04.03'

endDate = '2019.10.02'
s_page = 1
maxpage = 700
crawler1 = NaverNewsLister(s_page, maxpage , keyword, channel, startDate, endDate)
#crawler2 = NaverNewsLister(round((s_page+maxpage)/2), maxpage/2+1, keyword, channel, startDate, endDate)

crawler1.crawler()
#th2 = Thread(target=crawler2.crawler())

end = datetime.now()
