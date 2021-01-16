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
                     where='crawl_status="%s" and channel="navershopping" and task_id=24522'%(status))

for idx,task in enumerate(tasks):
    task_id = task['task_id']
    keyword = task['keyword']
    channel = task['channel']
    from_date = task['from_date']
    to_date = task['to_date']
    n_crawl = task['n_crawl']
    n_total = task['n_total']
    if n_total is not None and n_total>0:
        if channel == "navershopping":
            print("navershopping start")
            contents = db.select('crawl_contents', what='*',
                              where='crawl_status="%s" and task_id=%s' % (status,task_id))
            for idx,content in enumerate(contents):
                task_id = content['task_id']
                contents_id = content['contents_id']
                channel = channel
                title = content['title']
                n_reply = content['n_reply']
                prod_desc = json.loads(content['text'])
                if n_reply>0:
                    print(f"{contents_id} 에 대한 크롤링 시작 총 {n_reply} 의 리뷰")
                    crawl_review(contents_id,channel,title,from_date,to_date,n_reply,n_reply,prod_desc)
                else:
                    db.update_one('crawl_contents','n_reply_crawled',0,'contents_id',contents_id)
                    db.update_one('crawl_contents','crawl_status','GF','contents_id',contents_id)
                    continue
        else:
            print(idx, keyword,channel)
            crawl_contents(task_id,channel,keyword,from_date,to_date,n_crawl,n_total)

    else:
        continue
    db.update_one('crawl_task','crawl_status','GF','task_id',task_id)
    request = db.select('crawl_request AS cr '
              'JOIN crawl_request_task AS crt ON cr.request_id= crt.request_id '
              'JOIN crawl_task AS ct ON ct.task_id = crt.task_id',what='cr.request_id',where=f'ct.task_id={task_id}')
    request_id = request[0]['request_id']
    db.update_one('crawl_request', 'crawl_status', 'GF', 'request_id', request_id)

    print(task)
# crawl(keyword='손해보험',
#                 startDate='2020-08-01',
#                 endDate='2020-09-10',
#                 nCrawl=2000)
