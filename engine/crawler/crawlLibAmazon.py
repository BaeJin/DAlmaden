from sqlalchemy import create_engine
import re
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import time
from scrapy import Selector
import random
from engine.sql.almaden import Sql

class CrawlLibAmazon:
    def __init__(self,task_id=None ,keyword=None):
        self.CUSTOM_HEADER = {
            'authority': 'www.amazon.com',
            'cache-control': 'max-age=0',
            'rtt': '150',
            'downlink': '6.65',
            'ect': '4g',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'session-id=143-4184808-4175519; i18n-prefs=USD; sp-cdn=^\\^L5Z9:KR^\\^; ubid-main=131-3864953-3624011; lc-main=en_US; session-id-time=2082787201l; skin=noskin; session-token=uz+sSjctsGaz9Z0kfICd/5jj+MLUiJI1AAzdfKFGy9T6Zf0O2iNNEphijimeFK/A0HVsa6uS/YqRbUMslMprwn74seepAG3WHuC99IUr018zgf8MemEokh+HxcGX7T7RIA2vFUeIxDJpZSR9PD2uUhMdIbeq4pc8C4ipMndN0iVMpvrrHftyY1QSuyIAEWrl; csm-hit=adb:adblk_no^&t:1598336032599^&tb:2RBP3SA94EREVSD2TXNZ+s-2RBP3SA94EREVSD2TXNZ^|1598336032599',
        }

        self.engine = create_engine(
            ("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8").format
            ('root',
             'robot369',
             '1.221.75.76',
             3306,
             'datacast'),
            encoding='utf-8'
            )
        self.task_id = task_id
        self.keyword = keyword

    def crawl_total(self):
        find_text = "P.declare('s\-metadata',"
        find_script = None
        CATEGORY = self.keyword
        CATEGORY = CATEGORY.replace(" ", "+")
        db = Sql('datacast2')
        url = "https://www.amazon.com/s?k={}&ref=nb_sb_noss".format(CATEGORY)
        try:
            res = requests.get(url,headers=self.CUSTOM_HEADER)
            soup = BeautifulSoup(res.text, 'lxml')
            script_list = soup.find("div",{'id':'search'})
            script_list = script_list.find_all("script")
            for script in script_list:
                script = str(script)
                if find_text in script:
                    find_script = script
            data = re.sub('(<([^>]+)>)', '', find_script)
            data = data.replace("(","")
            data = data.replace(")", "")
            data = data.replace(";", "")
            data = data.replace("P.declare's\-metadata', ","")
            data = json.loads(data)
            nTotal = data["totalResultCount"]

            db.update_one('crawl_task', 'n_total', int(nTotal), 'task_id', self.task_id)

        except Exception as e:
            print(e)