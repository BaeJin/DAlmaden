import sys
sys.path.append('../')
from engine.crawler.db_utils import *
from engine.crawler._init_crawler import *
import json

db=Sql("datacast2")
status = "GR"
contents_row = db.select('crawling_status_youtube_view','*','contents_status="GR"')

for idx,row in enumerate(contents_row):
    keyword = row['keyword']
    task_id = row['task_id']
    channel = row['channel']
    contents_id = row['contents_id']
    title = row['title']
    n_reply = row['n_reply']
    prod_desc = json.loads(row['text'])
    real_contents_status =  db.select('crawling_status_youtube_view','*','contents_id="%s"'%(contents_id))
    real_contents_status = real_contents_status[0]['contents_status']
    if real_contents_status=='GR' and n_reply>0:
            print(f"{keyword}/{task_id}/{contents_id} 에 대한 크롤링 시작 총 {n_reply} 의 댓글")
            db.update_one('crawl_contents','crawl_status','GI','contents_id',contents_id)
            crawl_review(contents_id=contents_id,task_id=task_id,n_total=n_reply,prod_desc=prod_desc,channel=channel)
    elif real_contents_status=='GR' and n_reply<=0:
        db.update_one('crawl_contents','n_reply_crawled',0,'contents_id',contents_id)
        db.update_one('crawl_contents','crawl_status','GF','contents_id',contents_id)
    else:
        db.update_one('crawl_contents', 'crawl_status', 'GF', 'contents_id', contents_id)
