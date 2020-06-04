from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '광진구'                    ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
channel = 'Naver Blog'
startDate = '2018-07-01'
endDate = '2019-12-31'
ntotal = 2000

analyzer1 = TextAnalyzer(keyword, channel, startDate, \
                         endDate, "Mecab")
analyzer1.matching_sentiment_naver(ntotal)