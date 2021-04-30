import sys
from pathlib import Path
cwd = str(Path.cwd())
sys.path.append(cwd)
from engine.sql.almaden import Sql

db = Sql('datacast2')

request_rows = db.select('crawling_status_youtube_view',
                         '*','request_status!="SF" group by request_id')
for row in request_rows:
    request_id = row['request_id']
    request_status = row['request_status']
    task_id = row['task_id']
    contents = db.select('crawling_status_youtube_view',
                         'keyword,request_id,task_id,contents_id,request_status,task_status,contents_status',f'request_id={request_id}')

    ##reqeust_id 에 대한 contents 가 모두 크롤링이 끝낫을 때 reqeust 와 task 의 status 를 'GF' 로 변경(request 가 GR 인것에 대해서만)
    if all([content['contents_status'] == 'GF' for content in contents]) and request_status=='GR':
        db.update_one('crawling_status_youtube_view','task_status','GF','request_id',request_id)
        db.update_one('crawling_status_youtube_view','request_status','GF','request_id',request_id)
        print(f'req:{request_id},task:{task_id} is updated to GF')

    ##reqeust_id 에 대한 contents 가 모두 sentence 분석이 끝낫을 때 reqeust 와 task 의 status 를 'SF' 로 변경(request 가 GF 인것에 대해서만)
    elif all([content['contents_status'] == 'SF' for content in contents]) and request_status=='GF':
        db.update_one('crawling_status_youtube_view','task_status','SF','request_id',request_id)
        db.update_one('crawling_status_youtube_view','request_status','SF','request_id',request_id)
        print(f'req:{request_id},task:{task_id} is updated to SF')