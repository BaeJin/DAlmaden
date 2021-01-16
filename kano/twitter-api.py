import snscrape.modules.twitter as sntwitter
from datetime import datetime
keyword='코로나'
maxTweets=1000

st = datetime.now()
en = 0
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + 'since:2020-09-01 until:2020-09-25').get_items()) :
        print(i,tweet, tweet.date)
        if i > maxTweets :
            en = datetime.now()
            break

dt = en-st

print(dt)