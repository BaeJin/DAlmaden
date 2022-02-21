from google_play_scraper import Sort, reviews
import time
from engine.sql.almaden import Sql
from datetime import datetime
db = Sql("datacast2")

url_keyword = "com.lilithgames.rok.gpkr"
def start(count):
    result, continuation_token = reviews(
        url_keyword,
        lang='ko', # defaults to 'en'
        country='kr', # defaults to 'us'
        sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
        count=count, # defaults to 100
        filter_score_with=None # defaults to None(means all score)
    )
    return result, continuation_token

def iterator(count):
    result, continuation_token = start(count)
    yield result
    while True:
        result, continuation_token = reviews(
            url_keyword,
            continuation_token=continuation_token  # defaults to None(load from the beginning)
        )
        continuation_token = continuation_token
        yield result

error_count = 0
for idx, all_item in enumerate(iterator(100)):
    task_id = 156250
    item_batches = all_item
    for item in item_batches:
        try:
            print(item)
            response = item
            author = response["userName"]
            n_like = response["thumbsUpCount"]
            rating = int(response["score"])
            text = response["content"]
            post_date: datetime = response["at"]
            post_date: str = post_date.strftime("%Y-%m-%d")
            print(f"{idx}:{author}/{text}/{post_date}/{rating}/{n_like}")
        except Exception as e:
            print(f"{idx}:item not crawaled:{e}")
            if error_count <100:
                error_count += 1
                continue
            else:
                print(f"error, finish")
                break
        else:
            print(f"{idx}:item crawaled")
            db.insert("crawl_contents",
                      task_id=task_id,
                      author=author,
                      n_like=n_like,
                      rating=rating,
                      text=text,
                      post_date=post_date)

