from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '코로나'                    ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
sub_key = '코로나'
channel = 'All'
startDate = '2020-02-17'
endDate = '2020-02-23'
ntotal = 30000

analyzer1 = TextAnalyzer(keyword, channel, startDate, \
                         endDate, "Mecab", ntotal)
analyzer1.matching_sentiment_naver(sub_key, ntotal)