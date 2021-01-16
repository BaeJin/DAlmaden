from kano.engine import socialListening
import pandas as pd

#keyword , channel 설정하기
keywords_set_A = {'keyword': '전라도 김치', 'fromdate': '2010-01-01', 'todate': '2020-06-30', 'channel': 'naverblog'}

keywordA = keywords_set_A['keyword']
type = 'blog'
channel = keywords_set_A['channel']
lang = 'korean'
word_class = 'noun'
fromdate = keywords_set_A['fromdate']
todate = keywords_set_A['todate']
nurl = 2000
sl = socialListening.SocialListeing(keywordA, type, channel, lang, word_class=None, pos=None, fromdate= fromdate, todate = todate, nurl=nurl)

wc = socialListening.SlVizualize(sl)
wc.get_bow()
# _,dict_word_A = sl.get_bow()
