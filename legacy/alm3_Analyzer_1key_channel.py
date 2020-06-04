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

keyword1 ='곶자왈'


channel1 = 'Naver Blog'
channel2 = 'Instagram'
startDate = '2010-01-01'
endDate = '2019-12-31'

#### 각 키워드의 빈도표 보여주기A

analyzer1 = TextAnalyzer(keyword1, channel1, startDate, \
                        endDate, "Mecab")

dict1 = analyzer1.extractFrequentWords(500, 5)
print("<" + keyword1 + ">")
print(dict1)

wc1 = WordCloudRenderer(dict1, 'Dark2')

analyzer2 = TextAnalyzer(keyword1, channel2, startDate, \
                        endDate, "Mecab")
dict2 = analyzer2.extractFrequentWords(500, 5)
print("<" + keyword1 + ">")
print(dict2)

wc2 = WordCloudRenderer(dict2, 'tab10')

wc1.draw(1, keyword1+'_'+channel1)
wc2.draw(2, keyword1+'_'+channel2)

## 차이 분석 ##


sc = setCalc(dict1, dict2)
interdict = sc.getInter()
differa = sc.getDiff1()
differb = sc.getDiff2()

print("<%s - %s>" % (keyword1+'_'+channel1, keyword1+'_'+channel2))
print(differa)

print("<%s - %s>" % (keyword1+'_'+channel2, keyword1+'_'+channel1))
print(differb)

print("<intersection between %s and %s>" % (keyword1+'_'+channel2, keyword1+'_'+channel2))
print(interdict)

wc3 = WordCloudRenderer(differa, 'Dark2')
wc4 = WordCloudRenderer(differb, 'tab10')

wc3.draw(3, keyword1+'_'+channel1+'-'+keyword1+'_'+channel2)
wc4.draw(4, keyword1+'_'+channel2+'-'+keyword1+'_'+channel1)

###### 벤다이어그램 ######


wc5 = WordCloudRenderer(interdict, 'brg')
wc5.setMask("./mask_inter.png")

wc6 = WordCloudRenderer(differa, 'Dark2')
wc6.setMask("./mask_diff1.png")

wc7 = WordCloudRenderer(differb, 'tab10')
wc7.setMask("./mask_diff2.png")

# 교집합그림#
plt.figure(5, figsize=(16, 12))
plt.imshow(wc5.getWordCloud(), interpolation='bilinear')
plt.imshow(wc6.getWordCloud(), interpolation='bilinear')
plt.imshow(wc7.getWordCloud(), interpolation='bilinear')

plt.axis('off')
plt.savefig('image/inter/'+keyword1+'_'+channel2+'_inter_'+keyword1+'_'+channel1)
plt.show()