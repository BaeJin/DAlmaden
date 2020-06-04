from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus_3keywords import *
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword1 = '분유'

channel = 'Naver Blog'

startDate1 = '2005-01-01'
endDate1 = '2009-12-31'

startDate2 = '2010-01-01'
endDate2 = '2014-12-31'

startDate3 = '2015-01-01'
endDate3 = '2019-12-31'

nUrlA = 2000
nUrlB = 2000
nUrlC = 2000
#### 각 키워드의 빈도표 보여주기



analyzer1 = TextAnalyzer(keyword1, channel, startDate1,\
                         endDate1, "Mecab",nUrlA)
dict1=analyzer1.extractFrequentWords(500,5)

print("<"+keyword1+">")
print(dict1)

wc1 = WordCloudRenderer(dict1, 'Dark2')

analyzer2 = TextAnalyzer(keyword1, channel, startDate2,\
                         endDate2, "Mecab",nUrlB)
dict2=analyzer2.extractFrequentWords(500,5)

print("<"+keyword1+">")
print(dict2)

wc2 = WordCloudRenderer(dict2, 'tab10')

analyzer3 = TextAnalyzer(keyword1, channel, startDate3,\
                         endDate3, "Mecab",nUrlC)
dict3=analyzer3.extractFrequentWords(500,5)

print("<"+keyword1+">")
print(dict3)

wc3 = WordCloudRenderer(dict3, 'Dark2')


wc1.draw(1, keyword1+startDate1+"_"+endDate1)
wc2.draw(2, keyword1+startDate2+"_"+endDate2)
wc3.draw(3, keyword1+startDate3+"_"+endDate3)


## 차이 분석 ##


mins=0
inter_dict = {}
inter_list = []
key_set = dict1.keys()&dict2.keys()&dict3.keys()
print('key_set=',key_set)
for i in key_set:
    mins = min(dict1[i], dict2[i], dict3[i])
    inter_dict = {'keyword': i, 'count' : mins}
    inter_list.append(inter_dict)
inter_table = pd.DataFrame(inter_list, columns=('keyword', 'count'))
print(inter_table)
inter_table.to_excel(
    'keyword_sentiment_matching/inter/'+keyword1+startDate1+endDate1+'_inter_'+keyword1+startDate2+endDate2+'_inter_'+keyword1+startDate3+endDate3+'.xlsx',
    encoding="utf-8", index=True , engine='xlsxwriter')  # 엑셀에 저장한다. 대상 키워드와 비교년도 를 제목으로 하는 파일 생성

sc = setCalckey3(dict1, dict2, dict3)
interdictD = sc.getInterD()
interdictE = sc.getInterE()
interdictF = sc.getInterF()
interdictG = sc.getInterG()
differa = sc.getDiffA()
differb = sc.getDiffB()
differc = sc.getDiffC()



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
print("interdictE",interdictE)

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


#교집합그림#
plt.figure(4, figsize=(16,12))
plt.imshow(wc4.getWordCloud(), interpolation='bilinear')
plt.imshow(wc5.getWordCloud(), interpolation='bilinear')
plt.imshow(wc6.getWordCloud(), interpolation='bilinear')
plt.imshow(wc7.getWordCloud(), interpolation='bilinear')
plt.imshow(wc8.getWordCloud(), interpolation='bilinear')
plt.imshow(wc9.getWordCloud(), interpolation='bilinear')
plt.imshow(wc10.getWordCloud(), interpolation='bilinear')

plt.axis('off')
plt.savefig('image/inter/'+keyword1+startDate1+endDate1+'_inter_'+keyword1+startDate2+endDate2+'_inter_'+keyword1+startDate3+endDate3+"_all"+".png",transparent = True)

plt.show()
