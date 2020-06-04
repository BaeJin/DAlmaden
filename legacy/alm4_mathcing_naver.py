from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '롯데 자이언츠'                    ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
sub_key = '롯데'
channel = 'Naver Blog'
startDate = '2018-01-01'
endDate = '2018-12-31'
ntotal = 5000

analyzer1 = TextAnalyzer(keyword, channel, startDate, \
                         endDate, "Mecab", ntotal)
analyzer1.matching_sentiment_naver(ntotal, sub_key)