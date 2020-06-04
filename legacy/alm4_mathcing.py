from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer_sentiment import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '세븐나이츠'                   ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
channel = 'GooglePlay'
startDate = '2015-01-01'
endDate = '2019-12-31'
ntotal = 10000
analyzer1 = TextAnalyzer(keyword, channel, startDate, \
                         endDate, "Mecab", ntotal)
analyzer1.matching_sentiment_naver(ntotal)