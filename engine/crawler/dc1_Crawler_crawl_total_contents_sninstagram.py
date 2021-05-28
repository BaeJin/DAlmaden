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


twitter_serach_obj = sninstagram.InstagramHashtagScraper(mode="Hashtag",name="김치")
response = twitter_serach_obj.get_items()
print(response.)
