from polSeoul_total import *
from multiprocessing import Process, Pool
import sys
keyword = sys.argv[1]
channel = sys.argv[2]
startDate = sys.argv[3]
endDate = sys.argv[4]
quantity = 1000
pa = Pol_Analyzer(keyword, channel,quantity,startDate, endDate)
pa.pol_anaylze()
#pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
#pool.map(pa, ) # pool에 일을 던져줍니다.
