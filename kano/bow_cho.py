from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from collections import Counter
import pandas as pd
f = open("C:/Users/wodud/PycharmProjects/DAlmaden/kano/doc/iso_924.txt",'r',encoding='utf-8')
total_text = ''
total_text_list = []
lines = f.readlines()
pos = list()
for line in lines:
    pos.extend(pos_tag(word_tokenize(line)))

print(pos)
words = []
for p in pos:
    if p[1] in ['NN', 'NNP']:  # nltk
        words.append(p[0])
c = Counter(words)
c= c.most_common()

df = pd.DataFrame(c,columns=['keyword','count'])
df.to_excel('iso_924.xlsx',engine='xlsxwriter')