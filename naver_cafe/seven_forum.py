import requests
import json
import requests
from engine.sql.almaden import Sql
from datetime import datetime
import tzlocal
import pandas
import re

def html_remove(text):
    cleaned_text = re.compile('<.*?>')
    return re.sub(cleaned_text,'',text)

db =Sql("datacast2")

task_id = 28319

headers = {
    'authority': 'forum.netmarble.com',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://forum.netmarble.com/sk2/search/1?keyword=%EB%A0%88%EB%B3%BC%EB%A3%A8%EC%85%98',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_ga=GA1.2.1043831466.1611923525; _gid=GA1.2.1931761345.1611923525; _dc_gtm_UA-150068984-1=1',
}

for i in range(0,51):
    start = i*15
    contnet_params = {'rows':15, 'start':start, 'keyword':"레볼루션"}
    response = requests.get('https://forum.netmarble.com/api/game/sknightsmmo/official/forum/sk2/search/article/list', headers=headers, params=contnet_params)
    json_data = json.loads(response.text)
    article_list = json_data['articleList']
    for article in article_list:
        article_info = article
        article_id = article_info['id']
        forum_id = article_info['forumId']
        menu_seq = article_info['menuSeq']
        author = article_info['nickname']
        title = html_remove(article_info['title'])
        content = html_remove(article_info['nickname'])
        n_view = article_info['viewCount']
        timestamp = article_info['regDate']
        post_time = pandas.to_datetime(timestamp, unit='ms')
        post_datetime = post_time.strftime('%Y-%m-%d %H:%M:%S')
        post_date = post_time.strftime('%Y-%m-%d')
        print(post_datetime,post_date)
        url = f'https://forum.netmarble.com/{forum_id}/view/{menu_seq}/{article_id}'

        db.update_one("crawl_task","crawl_status","GR","task_id",task_id)
        db.insert("crawl_contents",
                      task_id=task_id,
                      url=url,
                      title=title,
                      text=content,
                      author=author,
                      post_time=post_datetime,
                      post_date=post_date,
                      n_view= n_view)

        review_param = {"start":0, "rows":'51','menuSeq':menu_seq,'articleId':article_id}
        review_response = requests.get(f'https://forum.netmarble.com/api/game/sknightsmmo/official/forum/sk2/article/{article_id}/comment/list?',params=review_param)
        review_response = json.loads(review_response.text)
        comment_list = review_response['commentList']
        for idx,comment in enumerate(comment_list):
            try:
                comment_info=comment
                reiview = html_remove(comment_info['content'])
                author = comment_info['nickname']
                timestamp = comment_info['regDate']
                post_time = pandas.to_datetime(timestamp, unit='ms')
                sentence_datetime = post_time.strftime('%Y-%m-%d %H:%M:%S')
                sentence_date = post_time.strftime('%Y-%m-%d')

                db.insert("crawl_contents",
                          task_id=task_id,
                          title=title,
                          text=reiview,
                          author=author,
                          post_time=sentence_datetime,
                          post_date=sentence_date,
                          is_reply=1)
            except:
                print(article_id,comment)