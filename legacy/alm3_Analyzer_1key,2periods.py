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





keyword1 = '스마트폰'


channel = 'Naver Blog'

startDate1 = '2010-01-01'
endDate1 = '2014-12-31'

startDate2 = '2015-01-01'
endDate2 = '2019-12-31'

nUrl = 5000
#### 각 키워드의 빈도표 보여주기

analyzer1 = TextAnalyzer(keyword1, channel, startDate1,\
                         endDate1, "Mecab", nUrl)
dict1=analyzer1.extractFrequentWords(500,5)
print("analyzing,,,")
print(dict1)


wc1 = WordCloudRenderer(dict1, 'Dark2')

analyzer2 = TextAnalyzer(keyword1, channel, startDate2,\
                         endDate2, "Mecab", nUrl)
dict2=analyzer2.extractFrequentWords(500,5)
print("analyzing,,,")
print(dict2)



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
plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 1, hspace = 0, wspace = 0)

plt.savefig('image/inter/'+keyword1+startDate1+endDate1+'_inter_'+keyword1+startDate2+endDate2, bbox_inces='tight',  pad_inches=0,
            dpi=100, transparent=True)
plt.show()

