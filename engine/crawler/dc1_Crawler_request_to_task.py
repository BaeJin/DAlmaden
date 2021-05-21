import sys
from pathlib import Path
cwd = str(Path.cwd())
sys.path.append(cwd)
from datetime import datetime
from engine.crawler.db_utils import *
import json
from engine.sql.almaden import Sql
db = Sql('datacast2')
b_to_rq = RequestTask()
b_to_rq.request_to_task()
# crawl(keyword='손해보험',XZ
#                 startDate='2020-08-01',
#                 endDate='2020-09-10',
#                 nCrawl=2000)
