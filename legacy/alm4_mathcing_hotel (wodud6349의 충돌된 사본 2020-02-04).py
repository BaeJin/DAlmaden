from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer_sentiment_hotel import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt


keyword = '호텔'                   ##function/function_keyword 엑셀파일에 해당하는  sheet 이름을 적어준다
channel = "Booking.com"

nUrl = 60000
analyzer1 = TextAnalyzer(keyword, channel,"Mecab")
analyzer1.matching_sentiment_naver(nUrl)