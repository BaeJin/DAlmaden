from threading import Thread
from crawlLibNaverBlog_12 import *
from textAnalyzer_multi import *
from renderWordCloud_CoronaTemplate import *
from setCalculus import *
import matplotlib.pyplot as plt

keyword1 = "코로나"
channel = 'Youtube'

startDate = '2020-02-16'
endDate = '2020-02-28'
nUrl = 8000
analyzer1 = TextAnalyzer(keyword1, channel, startDate, \
                         endDate, "Mecab",nUrl)
dict1 = analyzer1.extractFrequentWords(1000, 5)
#del dict1["코로나"]
#del dict1["필요"]
#del dict1["가능"]
#del dict1["사용"]
print("<" + keyword1 + ">")
print(dict1)
wc1 = WordCloudRenderer(dict1, 'Dark2')
# wc1.draw(1, keyword1)

plt.figure(5, figsize=(16, 12))
plt.imshow(wc1.getWordCloud(), interpolation='bilinear')
plt.axis('off')
plt.savefig('image/'+keyword1+"_"+startDate+"_"+endDate+"_all"+".png", transparent=True)

plt.show()
