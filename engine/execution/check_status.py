import sys
from pathlib import Path
project_dir = "/home/ubuntu/DAlmaden/"
sys.path.append(project_dir)
from engine.crawler.check_request_status_instagram import check_status_instagram
from engine.crawler.check_request_status_naverblog import check_status_naverblog
from engine.crawler.check_request_status_navershopping import check_status_navershopping

check_status_naverblog()
check_status_navershopping()
check_status_instagram()
