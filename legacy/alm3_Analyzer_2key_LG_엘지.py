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




keyword1 = '해외여행준비'
keyword2A = '체리쉬'
keyword2B = 'CHERISH'
channel = 'Naver Blog'

startDate = '2017-01-01'
endDate = '2019-12-31'


#### 각 키워드의 빈도표 보여주기

analyzer1 = TextAnalyzer(keyword1, channel, startDate,\
                         endDate, "Mecab", 3000)
dict1=analyzer1.extractFrequentWords(500,5)
print("<"+keyword1+">")
print(dict1)

wc1 = WordCloudRenderer(dict1, 'Dark2')

analyzer2A = TextAnalyzer(keyword2A, channel, startDate,\
                         endDate, "Mecab", 3000)
dict2A=analyzer2A.extractFrequentWords(500,5)
print("<"+keyword2A+">")

analyzer2B = TextAnalyzer(keyword2B, channel, startDate,\
                         endDate, "Mecab", 3000)
dict2B=analyzer2B.extractFrequentWords(500,5)
print("<"+keyword2B+">")

dict2 = {**dict2A, **dict2B}

print(dict2)

wc2 = WordCloudRenderer(dict2, 'tab10')


wc1.draw(1, keyword1)
wc2.draw(2, keyword2A)


## 차이 분석 ##



#sc = setCalc(dict1, dict2)
#interdict = sc.getInter()
#differa = sc.getDiff1()
#differb = sc.getDiff2()

#print("<%s - %s>" %(keyword1, keyword2))
#print(differa)

#print("<%s - %s>" %(keyword2, keyword1))
#print(differb)

#print("<intersection between %s and %s>"%(keyword2, keyword1))
#print(interdict)


#wc3 = WordCloudRenderer(differa, 'Dark2')
#wc4 = WordCloudRenderer(differb, 'tab10')


#wc3.draw(3)
#wc4.draw(4)


###### 벤다이어그램 ######

       
##wc5 = WordCloudRenderer(interdict, 'brg')
#wc5.setMask("./mask_inter.png")

#wc6 = WordCloudRenderer(differa, 'Dark2')
#wc6.setMask("./mask_diff1.png")

#wc7 = WordCloudRenderer(differb, 'tab10')
#wc7.setMask("./mask_diff2.png")




#교집합그림#
#plt.figure(5, figsize=(16,12))
#plt.imshow(wc5.getWordCloud(), interpolation='bilinear')
#plt.imshow(wc6.getWordCloud(), interpolation='bilinear')
#plt.imshow(wc7.getWordCloud(), interpolation='bilinear')

#plt.axis('off')

plt.show()

