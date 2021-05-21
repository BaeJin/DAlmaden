import requests
from bs4 import BeautifulSoup
import re
from engine.sql import almaden

db = almaden.Sql("datacast2")

page = 1
n_crawled = 0
contents_id = 11651711
while page <= 441:
    url = f"https://www.kurly.com/shop/goods/goods_review_list.php?goodsno=34055&page={page}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    for script in soup.find_all('strong'):
        script.extract()

    titles = soup.find_all('div',{'class':'fst'})
    reviews = soup.find_all('div',{'class':'inner_review'})

    for idx, review in enumerate(zip(titles,reviews)):
        n_crawled+=1
        db.update_one("crawl_contents", "n_reply_crawled", n_crawled, "contents_id", contents_id)

        title = review[0].text.replace('\n','')
        review_text = review[1].text.replace('\n','')
        print(title,review_text)
        title_plus_review = str(title)+ str(review_text)
        db.insert("crawl_sentence",
                  contents_id=contents_id,
                  seq=n_crawled,
                  sentence_type="review",
                  text=title_plus_review)
    page +=1