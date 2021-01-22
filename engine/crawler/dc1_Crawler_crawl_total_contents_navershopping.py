import sys
sys.path.append('../')
from engine.crawler.db_utils import *
from engine.crawler._init_crawler import *
import json
from multiprocessing import Process, Queue, freeze_support
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing

#등록된 task 의 상태를 확인하고 status 가 GR 인 task 를 가져와 크롤링 하기
db=Sql("datacast2")
status = "GR"
contents_row = db.select('crawling_status_navershopping_view','*','contents_status="GR"')

for idx,row in enumerate(contents_row):
    keyword = row['keyword']
    task_id = row['task_id']
    contents_id = row['contents_id']
    title = row['title']
    n_reply = row['n_reply']
    prod_desc = json.loads(row['text'])
    if n_reply>0:
            print(f"{keyword}/{task_id}/{contents_id} 에 대한 크롤링 시작 총 {n_reply} 의 리뷰")
            crawl_review(contents_id=contents_id,task_id=task_id,n_total=n_reply,prod_desc=prod_desc)
    else:
        db.update_one('crawl_contents','n_reply_crawled',0,'contents_id',contents_id)
        db.update_one('crawl_contents','crawl_status','GF','contents_id',contents_id)

    db.update_one('crawl_contents', 'crawl_status', 'GF', 'contents_id', contents_id)
