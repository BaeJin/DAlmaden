import json
from bs4 import BeautifulSoup
import requests
from exceptions import *
from engine.sql.almaden import *
from datetime import datetime


db = Sql("datacast2")
keyword = "누베베"

def get_keyhex(keyword):
    keyint = keyword.encode("UTF-8")
    keyhex = ""
    for i in keyint:
        keyhex = keyhex + '%{:02X}'.format(i)
    return keyhex
keyhex = get_keyhex(keyword)
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
    'referer': f'https://section.cafe.naver.com/ca-fe/home/search/articles?q={keyhex}&em=1',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_iframe_content_url(bs):
    try:
        iframe_content_list = bs.find_all("script", {"type": "text/javascript"})
        iframe_content = list(filter(lambda x: "//cafe.naver.com/ArticleRead.nhn?" in x.get_text(), iframe_content_list))
        iframe_content = iframe_content[0]
        iframe_text = iframe_content.get_text()
        iframe_text = iframe_text.split('$("cafe_main").src = "')[1]
        iframe_text = iframe_text.split('";')[0]
        article_number = iframe_text.split("art=")[0]
        article_number = article_number.split("articleid=")[1]
        article_number = article_number.split("&")[0]
        iframe_text = iframe_text.split("art=")[1]
        iframe_segment = iframe_text.split("&clubid=")
        iframe_url = f"https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{iframe_segment[1]}/articles/{article_number}?query=&art={iframe_segment[0]}"
        return iframe_url
    except Exception as e:
        print("get_iframe_content_error:",e)
        raise GetIframeContentError()
def get_text(json_data):
    content_html = json_data["result"]["article"]["contentHtml"]
    bs_content = BeautifulSoup(content_html, "lxml")
    text = bs_content.get_text()
    text = text.replace("※다이렉트결혼준비 비제휴업체의 홍보글, 후기글은 자동 삭제처리 될 수 있으며 지속될 시 등급 하향조정, 최대 카페 강제탈퇴 될 수 있습니다. ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    text = text.replace("\t", "")
    return text
def get_view(json_data):
    view = json_data["result"]["article"]["readCount"]
    return view
def get_comment_number(json_data):
    comment_number = json_data["result"]["article"]["commentCount"]
    return comment_number
def get_comments(json_data):
    items = json_data["result"]["comments"]["items"]
    comment = ""
    for item in items:
        comment += item["content"] if "추천인" not in item["content"] else ""
    return comment
def get_post_date(json_data):
    post_date = json_data["result"]["article"]["writeDate"]
    post_date = datetime.fromtimestamp(int(post_date)/1000)
    post_date = post_date.strftime("%Y-%m-%d")
    return post_date

def get_author(json_data):
    nickname = json_data["result"]["article"]["writer"]["nick"]
    return nickname

def get_title(json_data):
    title = json_data["result"]["article"]["subject"]
    return title

page = 1
num = 1

while True:
    keyword = "누베베"
    data = {"query": f"{keyword}", "page": page, "sortBy": 0, "exceptMarketArticle": 1, "period": ["20200101", "20211130"]}
    response = requests.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles', headers=headers,
                             json=data)
    json_data = json.loads(response.text)
    # total_content = json_data["message"]["result"]["totalCount"]
    post_list = json_data["message"]["result"]["searchResultArticle"]["searchResult"]

    if response.status_code == requests.codes.ok:
        for idx, post in enumerate(post_list):
            try:
                target_url = post["linkUrl"]
                response = requests.get(target_url)
                bs = BeautifulSoup(response.text,"lxml")
                iframe_url = get_iframe_content_url(bs)
                content_response = requests.get(url=iframe_url, params={"useCafeId": True, "requestFrom": "A"})

                json_data = json.loads(content_response.text)

                text = get_text(json_data)
                comment = get_comments(json_data)

                #####raw result
                all_text = text + comment
                all_text = all_text.replace("\n","")
                view = get_view(json_data)
                comment_number = get_comment_number(json_data)
                post_date = get_post_date(json_data)
                author = get_author(json_data)
                title = get_title(json_data)
                print(page, num, idx, all_text[0:10], view, comment_number, post_date, author, title)

            except Exception as e:
                print("error:",{e})
            else:
                num += 1
        page += 1
