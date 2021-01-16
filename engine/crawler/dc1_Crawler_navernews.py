import sys
sys.path.append('../')
from engine.crawler.crawlLibnavernews import CrawlLibnaverNews
from datetime import datetime


crawl_obj = CrawlLibnaverNews(1,keyword='알마덴',startDate='2019-01-01',endDate='2019-01-30')
crawl_obj.crawl_total()
# crawl(keyword='송전탑',
#                 startDate='2010-01-01',
#                 endDate='2020-12-03',
#                 nCrawl=100)

# naverblog.crawl(keyword='바나나',
#                 startDate='2020-01-01',
#                 endDate='2020-05-31',
#                 nCrawl = 5000)

# navershopping.crawl("전자담배",
#                     'https://smartstore.naver.com/ibholdings/products/4050389904?NaPm=ct%3Dkapcytsw%7Cci%3Ded4ec39f12b11008b2b8b38d4aa9754a14ad5590%7Ctr%3Dslsl%7Csn%3D791544%7Cic%3D%7Chk%3D11dd8f4f22874fda5fb99f3758fdc13f60935474',
#                     '궐련형 전자담배 죠즈20up jouz 아이코스3 듀오 릴플러스 차이코스 s 호환 20연타',
#                     comment="navershopping_test")

