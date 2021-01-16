from engine.sql.almaden import Sql

import requests
import json
import scrapy
from bs4 import BeautifulSoup
import re
import time

HASH_KEY = "graphql"
HASHTAG_KEY = "hashtag"
MEDIA_KEY = "edge_hashtag_to_media"
LIST_KEY = "edges"
NODE_KEY = "node"
CAPTION_LIST_KEY = "edge_media_to_caption"
TEXT_KEY = "text"
COUNT_KEY = "count"

class CrawlLibInstagram:

    def __init__(self,task_id=None,keyword=None,num_content=None):

        self.task_id = task_id
        self.keyword = keyword.replace(" ","")
        self.num_content = num_content
        self.db = Sql('datacast2')
        self.headers = {
        'authority': 'www.instagram.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'ig_did=137A7314-981D-4654-8FA0-F756EFECC7CA; mid=X9iuSAALAAH0n37lLiuZbMevZOZG; ig_nrcb=1; shbid=7030; shbts=1608035927.8347807; csrftoken=kYaVmMQIRyyHmNDaKs33hB8iY4cnKo0n; ds_user_id=1945681515; sessionid=1945681515%3AZgzAhVmzgdNEzw%3A3; rur=FTW; urlgen="{\\"1.221.75.76\\": 3786}:1kpRyZ:4gBqpzOQ4Jjdbo1GLlIdt0Ts-Ys"',
        }

    def get_url(self):
        # api_key = "2c5b500fff718ba1c67f02eb21e79358"
        # url = f"http://api.scraperapi.com?api_key={api_key}&url={instagram_target_url}"
        url = "https://www.instagram.com/explore/tags/" +self.keyword + "/?__a=1"
        return url

    def get_request_response(self):
        r = requests.get(url=self.get_url())
        print(r.text)

        data = r.json()
        return data

    def crawl_total(self):
        data = self.get_request_response()
        nTotal = data[HASH_KEY][HASHTAG_KEY][MEDIA_KEY][COUNT_KEY]
        self.db.update_one('crawl_task','n_total',nTotal,'task_id',self.task_id)


    def start_requests(self):
        keyword = self.keyword
        print(keyword)
        #유저이름에 대한 contents 검색 https://www.instagram.com/<user_name>/
        #https://www.instagram.com/explore/locations/< location_id >
        #Tags URL
        #나라 설정은 parameter : hl 이용 ex)https://www.instagram.com/nike/?hl=en  #English

        instagram_target_url = f'https://www.instagram.com/explore/tags/{keyword}'
        response = requests.get(self.get_url(instagram_target_url))
        return self.parse(response)


    def parse(self,response):

        response_html = response.text
        soup = BeautifulSoup(response_html,'lxml')
        source_page_soup = soup.find('script', text=re.compile("window._sharedData = "))
        source_page_script = str(source_page_soup)
        json_string = source_page_script.strip().split('= ')[-1]
        json_string = json_string.replace(";</script>","")
        data = json.loads(json_string)

        ##가져온 json 형태의 데이터에서 필요한 데이터만 추출하면 됨
        print(data['entry_data'])
        # next_page_bool = \
        #     data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
        #         'has_next_page']
        # print(next_page_bool)

        time.sleep(10000)