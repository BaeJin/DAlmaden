import json
from bs4 import BeautifulSoup
import requests
from exceptions import *
from engine.sql.almaden import *
from datetime import datetime

headers = {
    'authority': 'apis.naver.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'accept': 'application/json, text/plain, */*',
    'x-cafe-product': 'pc',
    'content-type': 'application/json;charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'origin': 'https://section.cafe.naver.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://section.cafe.naver.com/ca-fe/home/search/articles?q=%EB%88%84%EB%B2%A0%EB%B2%A0&em=1',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}
keyword = "누베베"
page = 1
data = {"query": f"{keyword}", "page": page, "sortBy": 0, "exceptMarketArticle": 1, "period": ["20200101", "20211130"]}
response = requests.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles', headers=headers,
                         json=data)
json_data = json.loads(response.text)
total_content = json_data["message"]["result"]["totalCount"]
print(total_content)