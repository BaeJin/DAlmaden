import time
from datetime import datetime
import steamreviews
from engine.sql.almaden import Sql

request_params = dict()
request_params['filter'] = 'funny'
app_id = 289070
task_id = 156246
db = Sql("datacast2")
for response in steamreviews.download_reviews_for_app_id(app_id, chosen_request_params=request_params):
    item_list = response[0]
    for item in item_list:
        author = item["author"]
        text = item["review"]
        n_like = item["votes_up"]
        n_reply = item["comment_count"]
        n_funny = item["votes_funny"]
        post_date: datetime = datetime.fromtimestamp(item["timestamp_updated"])
        post_date: str = post_date.strftime("%Y-%m-%d")
        print(post_date)
        db.insert("crawl_contents",
                  task_id=task_id,
                  author=str(author),
                  n_like=n_like,
                  text=text,
                  post_date=post_date)
    time.sleep(0.5)