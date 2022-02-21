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
                     where='crawl_status="%s" and channel="naverblog"'%(status))

for idx,task in enumerate(tasks):
    try:
        task_id = task['task_id']
        keyword = task['keyword']
        channel = task['channel']
        from_date = task['from_date']
        to_date = task['to_date']
        n_crawl = task['n_crawl']
        n_total = task['n_total']
        real_crawl_status = db.select('crawl_task',what ='*',
                         where='task_id="%s"'%(task_id))
        real_crawl_status= real_crawl_status[0]['crawl_status']
        if real_crawl_status=='GR' and n_total is not None and n_total>0:
            print(idx, keyword,channel)
            db.update_one('crawl_task','crawl_status','GI','task_id',task_id)
            crawl_contents(task_id,channel,keyword,from_date,to_date,n_crawl,n_total)
            db.update_one('crawl_task','crawl_status','GF','task_id',task_id)
        elif real_crawl_status=='GR' and n_total is not None and n_total==0:
            db.update_one('crawl_task','n_crawled',0,'task_id',task_id)
            db.update_one('crawl_task','crawl_status','GF','task_id',task_id)
        else:
            db.update_one('crawl_task','crawl_status','GF','task_id',task_id)
    except Exception as e:
        print(e)

        db = Sql("datacast2")
        status = "GR"
        tasks = db.select('crawl_task', what='*',
                          where='crawl_status="%s" and channel="naverblog"' % (status))
        continue
# crawl(keyword='손해보험',
#                 startDate='2020-08-01',
#                 endDate='2020-09-10',
#                 nCrawl=2000)
