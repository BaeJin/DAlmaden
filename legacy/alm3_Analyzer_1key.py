from threading import Thread
from crawlLibNaverBlog import *
from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt
import gc
import matplotlib
keyword1 = "전자담배"

channel = "Naver Blog"

startDate = '2020-01-01'
endDate = '2020-12-31'
nUrl = 5000
analyzer1 = TextAnalyzer(keyword1,channel, startDate, \
                         endDate, "Mecab",nUrl)
dict1 = analyzer1.extractFrequentWords(500, 5)

print("<" + keyword1 + ">")

print(dict1)
wc1 = WordCloudRenderer(dict1, 'Dark2')
# wc1.draw(1, keyword1)

plt.figure(5, figsize=(16, 12))
plt.imshow(wc1.getWordCloud(), interpolation='bilinear')

plt.axis('off')
plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 1, hspace = 0, wspace = 0)

plt.savefig('image/'+keyword1+"_"+startDate+"_"+endDate+"_all"+".png",bbox_inces='tight',  pad_inches=0,
            dpi=100, transparent=True)

plt.show()
print('finish')