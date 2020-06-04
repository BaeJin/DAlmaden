from threading import Thread
from crawlLibNaverBlog_12 import *
from seven_num import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '세븐나이츠'                   ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
channel = 'GooglePlay'
startDate = '2016-01-01'
endDate = '2020-01-31'
nUrl = 10000
analyzer1 = TextAnalyzer(keyword, channel, startDate, \
                         endDate, "Mecab",nUrl)
analyzer1.matching_sentiment_naver(nUrl)