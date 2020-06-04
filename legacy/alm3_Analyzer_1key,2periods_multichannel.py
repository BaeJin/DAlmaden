from threading import Thread
#from crawlLibNaverBlog import *
from textAnalyzer_multi import *
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





keyword1 = '코로나'


channel = 'multi'

startDate1 = '2020-01-01'
endDate1 = '2020-01-31'

startDate2 = '2020-02-01'
endDate2 = '2020-02-28'


#### 각 키워드의 빈도표 보여주기

analyzer1 = TextAnalyzer(keyword1, channel, startDate1,\
                         endDate1, "Mecab", 2000)
dict1=analyzer1.extractFrequentWords(500,5)
print("analyzing,,,")
print(dict1)
del dict1['코로나']
#del dict1['천사','분양','강아지']
wc1 = WordCloudRenderer(dict1, 'Dark2')

analyzer2 = TextAnalyzer(keyword1, channel, startDate2,\
                         endDate2, "Mecab", 2000)
dict2=analyzer2.extractFrequentWords(500,5)
print("analyzing,,,")
print(dict2)
del dict2['코로나']
wc2 = WordCloudRenderer(dict2, 'tab10')


wc1.draw(1, keyword1+startDate1+"_"+endDate1)
wc2.draw(2, keyword1+startDate2+"_"+endDate2)



## 차이 분석 ##



sc = setCalc(dict1, dict2)
interdict = sc.getInter()
differa = sc.getDiff1()
differb = sc.getDiff2()

##print("<%s - %s>" %(keyword1, keyword2))
print(differa)

##print("<%s - %s>" %(keyword2, keyword1))
print(differb)

##print("<intersection between %s and %s>"%(keyword2, keyword1))
print(interdict)


wc3 = WordCloudRenderer(differa, 'Dark2')
wc4 = WordCloudRenderer(differb, 'tab10')


wc3.draw(3, keyword1+startDate1+"_"+endDate1+'-'+keyword1+startDate2+"_"+endDate2)
wc4.draw(4, keyword1+startDate2+"_"+endDate2+'-'+keyword1+startDate1+"_"+endDate1)


###### 벤다이어그램 ######

       
wc5 = WordCloudRenderer(interdict, 'brg')
wc5.setMask("./mask_inter.png")

wc6 = WordCloudRenderer(differa, 'Dark2')
wc6.setMask("./mask_diff1.png")

wc7 = WordCloudRenderer(differb, 'tab10')
wc7.setMask("./mask_diff2.png")




#교집합그림#
plt.figure(5, figsize=(16,12))
plt.imshow(wc5.getWordCloud(), interpolation='bilinear')
plt.imshow(wc6.getWordCloud(), interpolation='bilinear')
plt.imshow(wc7.getWordCloud(), interpolation='bilinear')

plt.axis('off')
plt.savefig('image/inter/'+keyword1+startDate1+endDate1+'_inter_'+keyword1+startDate2+endDate2)
plt.show()

