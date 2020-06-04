from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer_google import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '호텔'                   ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
channel = 'booking.com'
startDate = '2010-01-01'
endDate = '2014-12-31'
nUrl = 60000
analyzer1 = TextAnalyzer(keyword, channel, startDate, \
                         endDate, "Mecab",nUrl)
analyzer1.matching_sentiment_naver(nUrl)