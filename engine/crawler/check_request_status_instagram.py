import sys
from pathlib import Path
cwd = str(Path.cwd())
sys.path.append(cwd)
from engine.sql.almaden import Sql

def check_status_instagram():
    db = Sql('datacast2')

    request_rows = db.select('crawl_request','*','task_ids is not null')

    for row in request_rows:
        request_id = row['request_id']
        task_ids = db.select('crawl_request as cr '
                             'join crawl_request_task as crt on cr.request_id=crt.request_id '
                             'join crawl_task as ct on ct.task_id=crt.task_id',
                             'cr.request_id,ct.task_id,ct.crawl_status',f'cr.request_id={request_id}')

        if all([task['crawl_status'] == 'GF' for task in task_ids]):
            db.update_one('crawl_request','crawl_status','GF','request_id',request_id)
            print(f'insta,req:{request_id} is updated to GF')

        elif all([task['crawl_status'] == 'SF' for task in task_ids]):
            db.update_one('crawl_request','crawl_status','SF','request_id',request_id)
            print(f'insta,req:{request_id} is updated to SF')
