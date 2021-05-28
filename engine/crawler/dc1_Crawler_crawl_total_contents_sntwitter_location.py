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

keyword = "lg"
n_crawl = 10000
from_date = "2019-01-01"
to_date = "2021-01-31"

place_id = None #"96683cc9126741d1"
twitter_serached_items = sntwitter.TwitterSearchScraper(f"{keyword} since:{from_date} until:{to_date} :usa").get_items()
for idx,tweet in enumerate(twitter_serached_items):
    content = re.sub('\n','',tweet.content)
    print(idx, tweet.url,content,tweet.date)
    if idx >= n_crawl:
        break