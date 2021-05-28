import twitter
import numpy as np
import pandas as pd
import string
import re
import os
import snscrape
import snscrape.modules.twitter as sntwitter
import snscrape.modules.instagram as sninstagram
from time import sleep
import datetime

keyword = "나서스"
n_crawl = 10000
from_date = "2019-01-01"
to_date = "2019-01-31"
twitter_serached_items = sntwitter.TwitterSearchScraper(f"{keyword} since:{from_date} until:{to_date}").get_items()
for idx,tweet in enumerate(twitter_serached_items):
    content = re.sub('\n','',tweet.content)
    print(idx, tweet.url,content,tweet.date)
    if idx >= n_crawl:
        break