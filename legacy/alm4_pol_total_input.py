from polSeoul_total import *
from multiprocessing import Process, Pool
keyword = "코오롱스포츠"
channel = "Instagram"
startDate = "2019-09-01"
endDate = "2019-09-31"
quantity = 1000
pa = Pol_Analyzer(keyword, channel,quantity,startDate, endDate)
p = Process(target=pa.pol_anaylze())
p.start()
p.join()
#pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
#pool.map(pa, ) # pool에 일을 던져줍니다.
