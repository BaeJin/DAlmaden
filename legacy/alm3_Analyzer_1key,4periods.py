from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus_4keywords import *
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



keyword = '코로나'


channel = 'Naver Blog'

startDate1 = '2020-01-01'
endDate1 = '2020-01-15'

startDate2 = '2020-01-16'
endDate2 = '2020-01-31'

startDate3 = '2020-02-01'
endDate3 = '2020-02-15'

startDate4 = '2020-02-16'
endDate4 = '2020-02-26'
u = 3000
#### 각 키워드의 빈도표 보여주기

analyzer1 = TextAnalyzer(keyword, channel, startDate1,\
                         endDate1, "Mecab", u)
dict1=analyzer1.extractFrequentWords(500,5)
print("<"+startDate1+"~"+endDate1+">")
print(dict1)

wc1 = WordCloudRenderer(dict1, 'Dark2')

analyzer2 = TextAnalyzer(keyword, channel, startDate2,\
                         endDate2, "Mecab", u)
dict2=analyzer2.extractFrequentWords(500,5)
print("<"+startDate2+"~"+endDate2+">")
print(dict2)

wc2 = WordCloudRenderer(dict2, 'tab10')

analyzer3 = TextAnalyzer(keyword, channel, startDate3,\
                         endDate3, "Mecab", u)
dict3=analyzer3.extractFrequentWords(500,5)
print("<"+startDate3+"~"+endDate3+">")
print(dict3)

wc3 = WordCloudRenderer(dict3, 'Dark2')

analyzer4 = TextAnalyzer(keyword, channel, startDate4,\
                         endDate4, "Mecab", u)
dict4=analyzer4.extractFrequentWords(500,5)
print("<"+startDate4+"~"+endDate4+">")
print(dict4)

wc4 = WordCloudRenderer(dict4, 'Dark2')


## 차이 분석 ##



sc = setCalckey4(dict1, dict2, dict3, dict4)
interdictE=sc.getInterE()
interdictF=sc.getInterF()
interdictG=sc.getInterG()
interdictH=sc.getInterH()
interdictI=sc.getInterI()
interdictJ=sc.getInterJ()
interdictK=sc.getInterK()
interdictL=sc.getInterL()
interdictM=sc.getInterM()
differA=sc.getDiffA()
differB=sc.getDiffB()
differC=sc.getDiffC()
differD=sc.getDiffD()


print("getting results..")


###### 벤다이어그램 ######

       
wc5 = WordCloudRenderer(differA, 'Dark2')
wc5.setMask("./mask4new_A.png")

wc6 = WordCloudRenderer(differB, 'tab10')
wc6.setMask("./mask4new_B.png")

wc7 = WordCloudRenderer(differC, 'Dark2')
wc7.setMask("./mask4new_C.png")

wc8 = WordCloudRenderer(differD, 'brg')
wc8.setMask("./mask4new_D.png")

wc9 = WordCloudRenderer(interdictE, 'tab10')
wc9.setMask("./mask4new_E.png")

wc10 = WordCloudRenderer(interdictF, 'brg')
wc10.setMask("./mask4new_F.png")

wc11 = WordCloudRenderer(interdictG, 'Dark2')
wc11.setMask("./mask4new_G.png")

wc12 = WordCloudRenderer(interdictH, 'brg')
wc12.setMask("./mask4new_H.png")

wc13 = WordCloudRenderer(interdictI, 'tab10')
wc13.setMask("./mask4new_I.png")

wc14 = WordCloudRenderer(interdictJ, 'brg')
wc14.setMask("./mask4new_J.png")

wc15 = WordCloudRenderer(interdictK, 'tab10')
wc15.setMask("./mask4new_K.png")

wc16 = WordCloudRenderer(interdictL, 'brg')
wc16.setMask("./mask4new_L.png")

wc17 = WordCloudRenderer(interdictM, 'Dark2')
wc17.setMask("./mask4new_M.png")


#교집합그림#
plt.figure(5, figsize=(16,12))
plt.imshow(wc5.getWordCloud(), interpolation='bilinear')
plt.imshow(wc6.getWordCloud(), interpolation='bilinear')
plt.imshow(wc7.getWordCloud(), interpolation='bilinear')
plt.imshow(wc8.getWordCloud(), interpolation='bilinear')
plt.imshow(wc9.getWordCloud(), interpolation='bilinear')
plt.imshow(wc10.getWordCloud(), interpolation='bilinear')
plt.imshow(wc11.getWordCloud(), interpolation='bilinear')
plt.imshow(wc12.getWordCloud(), interpolation='bilinear')
plt.imshow(wc13.getWordCloud(), interpolation='bilinear')
plt.imshow(wc14.getWordCloud(), interpolation='bilinear')
plt.imshow(wc15.getWordCloud(), interpolation='bilinear')
plt.imshow(wc16.getWordCloud(), interpolation='bilinear')
plt.imshow(wc17.getWordCloud(), interpolation='bilinear')

plt.axis('off')

plt.show()
