from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt

########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################




keyword1A = '서울 일자리'
channel = 'Naver Blog'

startDate1 = '2015-01-01'
endDate1 = '2017-06-30'




#### 각 키워드의 빈도표 보여주기

analyzer1A = TextAnalyzer(keyword1A, channel, startDate1,\
                         endDate1, "Mecab")
dict1A=analyzer1A.extractFrequentWords(500,5)
print("<"+keyword1A+">")
print(dict1A)



analyzer1B = TextAnalyzer(keyword1B, channel, startDate2,\
                         endDate2, "Mecab")
dict1B=analyzer1B.extractFrequentWords(500,5)
print("<"+keyword1A+">")
print(dict1B)


dict1={**dict1A , **dict1B}

wc1 = WordCloudRenderer(dict1, 'Dark2')


wc1.draw(1, keyword1A)



#### 차이 분석 ##
##
##
##
##sc = setCalc(dict1, dict2)
##interdict = sc.getInter()
##differa = sc.getDiff1()
##differb = sc.getDiff2()
##
##print("<%s - %s>" %(keyword1, keyword2))
##print(differa)
##
##print("<%s - %s>" %(keyword2, keyword1))
##print(differb)
##
##print("<intersection between %s and %s>"%(keyword2, keyword1))
##print(interdict)
##
##
##wc3 = WordCloudRenderer(differa, 'Dark2')
##wc4 = WordCloudRenderer(differb, 'tab10')
##
##
##wc3.draw(3)
##wc4.draw(4)
##
##
######## 벤다이어그램 ######
##
##       
##wc5 = WordCloudRenderer(interdict, 'brg')
##wc5.setMask("./mask_inter.png")
##
##wc6 = WordCloudRenderer(differa, 'Dark2')
##wc6.setMask("./mask_diff1.png")
##
##wc7 = WordCloudRenderer(differb, 'tab10')
##wc7.setMask("./mask_diff2.png")
##
##
##
##
###교집합그림#
##plt.figure(5, figsize=(16,12))
##plt.imshow(wc5.getWordCloud(), interpolation='bilinear')
##plt.imshow(wc6.getWordCloud(), interpolation='bilinear')
##plt.imshow(wc7.getWordCloud(), interpolation='bilinear')
##
plt.axis('off')
##
plt.show()
##
##
