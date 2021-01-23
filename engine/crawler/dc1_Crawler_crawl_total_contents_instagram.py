import sys
sys.path.append('../')
from engine.crawler.db_utils import *
from engine.crawler.crawlLibnaverblog import *
from engine.crawler._init_crawler import *
import json
from multiprocessing import Process, Queue, freeze_support
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing

#등록된 task 의 상태를 확인하고 status 가 GR 인 task 를 가져와 크롤링 하기
db=Sql("datacast2")
status = "GR"
tasks = db.select('crawl_task',what ='*',
                     where='crawl_status="%s" and channel="instagram"'%(status))

for idx,task in enumerate(tasks):
    task_id = task['task_id']
    keyword = task['keyword']
    channel = task['channel']
    from_date = task['from_date']
    to_date = task['to_date']
    n_crawl = task['n_crawl']
    n_total = task['n_total']
    if n_total is not None and n_total>0:
        print(idx, keyword,channel)
        crawl_contents(task_id,channel,keyword,from_date,to_date,n_crawl,n_total)
        db.update_one('crawl_task','crawl_status','GF','task_id',task_id)
    else:
        continue

