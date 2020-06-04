from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '코로나'                    ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
sub_key = '코로나'
channel = 'All'
startDate = '2020-01-20'
endDate = '2020-01-26'
ntotal = 5000
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-01-06" "2019-01-12" "2000"
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-01-13" "2019-01-19" "2000"
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-01-20" "2019-01-26" "2000"
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-01-27" "2019-02-02" "2000"
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-02-03" "2019-02-09" "2000"
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-02-10" "2019-02-16" "2000"
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-02-17" "2019-02-23" "2000"
# python alm1_UrlLister_1key_YouTube_batch.py "코로나" "YouTube" "2019-02-24" "2019-02-25" "2000"
analyzer1 = TextAnalyzer(keyword, channel, startDate, \
                         endDate, "Mecab", ntotal)
analyzer1.matching_sentiment_youtube(ntotal, sub_key)