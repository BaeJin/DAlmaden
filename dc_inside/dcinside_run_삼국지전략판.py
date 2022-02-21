from dcinside import crawler
from engine.sql.almaden import Sql

db = Sql("datacast2")
dc_crawler = crawler.Crawler()


task_id = 156247
batch_size = 5
for i in range(1, 83000, batch_size):
    response = dc_crawler.crawl(gallery="3kingdoms", idx=i, batch_size=batch_size)
    print(f"{i}:{response}")
    if "error" in response.keys():
        continue
    db.insert("crawl_contents",
              task_id= task_id,
              title=response["title"],
              text=response["text"],
              author=response["author"],
              post_date=response["post_date"],
              review=str(response["review"]),
              n_view=response["n_view"],
              n_like=response["n_like"],
              url=response["url"])
