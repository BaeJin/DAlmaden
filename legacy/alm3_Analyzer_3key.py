from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer2 import *
from renderWordCloud import *
from setCalculus_3keywords import *
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


keyword1 = '풀무원 만두'
keyword2 = '인공눈물 보호'
keyword3 = '인공눈물 피로'

channel = 'Naver Blog'

startDate = '2010-01-01'
endDate = '2020-01-21'
nUrlA = 3000
nUrlB = 3000
nUrlC = 3000

#### 각 키워드의 빈도표 보여주기

analyzer1 = TextAnalyzer(keyword1, channel, startDate, \
                         endDate, "Mecab", nUrlA)
dict1 = analyzer1.extractFrequentWords(500, 5)
print("<" + keyword1 + ">")
print(dict1)
wc1 = WordCloudRenderer(dict1, 'Dark2')

analyzer2 = TextAnalyzer(keyword2, channel, startDate, \
                         endDate, "Mecab", nUrlB)
dict2 = analyzer2.extractFrequentWords(500, 5)
print("<" + keyword2 + ">")
print(dict2)

wc2 = WordCloudRenderer(dict2, 'tab10')

analyzer3 = TextAnalyzer(keyword3, channel, startDate, \
                         endDate, "Mecab", nUrlC)
dict3 = analyzer3.extractFrequentWords(500, 5)
print("<" + keyword3 + ">")
print(dict3)

wc3 = WordCloudRenderer(dict3, 'Dark2')

wc1.draw(1, keyword1)
wc2.draw(2, keyword2)
wc3.draw(3, keyword3)

## 차이 분석 ##


sc = setCalckey3(dict1, dict2, dict3)
interdictD = sc.getInterD()
interdictE = sc.getInterE()
interdictF = sc.getInterF()
interdictG = sc.getInterG()
differa = sc.getDiffA()
differb = sc.getDiffB()
differc = sc.getDiffC()

print("<%s - (%s + %s)>" % (keyword1, keyword2, keyword3))
print(differa)

print("<%s - (%s + %s)>" % (keyword2, keyword1, keyword3))
print(differb)

print("<%s - (%s + %s)>" % (keyword3, keyword1, keyword2))
print(differc)

print("getting intersections,,,")
##print("<intersection between %s and %s>"%(keyword1, keyword2))
##print(interdict)


##wc3 = WordCloudRenderer(differa, 'Dark2')
##wc4 = WordCloudRenderer(differb, 'tab10')
##
##
##wc3.draw(3)
##wc4.draw(4)

###### 벤다이어그램 ######


wc4 = WordCloudRenderer(interdictD, 'tab10')
wc4.setMask("./mask3_D(inter1).png")

wc5 = WordCloudRenderer(interdictE, 'Dark2')
wc5.setMask("./mask3_E(inter2).png")

wc6 = WordCloudRenderer(interdictF, 'tab10')
wc6.setMask("./mask3_F(inter3).png")

wc7 = WordCloudRenderer(interdictG, 'brg')
wc7.setMask("./mask3_G(inter4).png")

wc8 = WordCloudRenderer(differa, 'Dark2')
wc8.setMask("./mask3_A(diff1).png")
wc9 = WordCloudRenderer(differb, 'tab10')
wc9.setMask("./mask3_B(diff2).png")

wc10 = WordCloudRenderer(differc, 'Dark2')
wc10.setMask("./mask3_C(diff3).png")

# 교집합그림#
plt.figure(4, figsize=(16, 12))
plt.imshow(wc4.getWordCloud(), interpolation='bilinear')
plt.imshow(wc5.getWordCloud(), interpolation='bilinear')
plt.imshow(wc6.getWordCloud(), interpolation='bilinear')
plt.imshow(wc7.getWordCloud(), interpolation='bilinear')
plt.imshow(wc8.getWordCloud(), interpolation='bilinear')
plt.imshow(wc9.getWordCloud(), interpolation='bilinear')
plt.imshow(wc10.getWordCloud(), interpolation='bilinear')

plt.axis('off'), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 1, hspace = 0, wspace = 0)

plt.savefig('image/inter/' + keyword1 + '_inter_' + keyword2 + '_inter_' + keyword3 + ".png", bbox_inces='tight',  pad_inches=0,
            dpi=100, transparent=True)

plt.show()
