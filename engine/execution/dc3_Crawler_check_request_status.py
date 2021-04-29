import sys
from pathlib import Path
cwd = str(Path.cwd())
# print(Path.cwd().parents[1])
# print(type(Path.cwd().parents[1]))
sys.path.append(Path.cwd().parents[1])
print(sys.path)
from engine.crawler.check_request_status_instagram import check_status_instagram
from engine.crawler.check_request_status_naverblog import check_status_naverblog
from engine.crawler.check_request_status_navershopping import check_status_navershopping


# check_status_naverblog()
# check_status_navershopping()
# check_status_instagram()
# check_status_instagram()