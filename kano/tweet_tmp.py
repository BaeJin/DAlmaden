import pandas as pd
from kano.lib.wordcloud.setCalculus import setCalc, setCalckey3
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import snscrape.modules.twitter as sntwitter
import itertools
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk import FreqDist
import re
from pathlib import Path
import numpy as np

rc('font',family='malgun gothic')

stopKeywordList = stopwords.words('english')
stopKeywordList.append("https")
dir = Path.cwd()
fontname = 'NanumBarunGothic.ttf'


def draw_to_imshow(dict, palette=None, maskPic=None):
    if maskPic == None:
        maskPic = np.array(Image.open(str(dir) + "/source/img/" + "mask.png"))
    else:
        maskPic = np.array(Image.open(str(dir) + "/source/img/" + maskPic))

    wordcloud = WordCloud(font_path=str(dir) + "/source/fonts/" + fontname, \
                          background_color="rgba(255,255,255,0)", mode='RGBA', \
                          max_font_size=120, \
                          min_font_size=18, \
                          mask=maskPic, \
                          width=200, height=200, \
                          colormap=palette) \
        .generate_from_frequencies(dict)

    return wordcloud, maskPic


def analyaze_tweets(keyword,loc,since,until,coord):
    df_coord = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
        '{} near:"{}" since:{} until:{}'.format(keyword,coord,since,until)).get_items(), 5000))[['user', 'date','content']]

    df_coord['search_keyword'] = keyword
    df_coord['user_location'] = df_coord['user'].apply(lambda x: x['location'])
    df_coord['date'] = df_coord['date'].apply(lambda a: pd.to_datetime(a).date())
    len_df = len(df_coord)
    df_coord.to_excel(f"results/{keyword}_{loc}_{since}_{until}_{len_df}_tweets.xlsx")

    word_class_list = ['NN', 'NNS', 'NNP', 'NNPS']
    pos = list()
    words = list()
    remove_list = pos_tag(keyword)
    for idx in df_coord.index:
        pos.extend(pos_tag(word_tokenize(df_coord.at[idx,'content'])))

    for p in pos:
        if p[0] not in remove_list and p[1] in word_class_list:  # nltk
            words.append(p[0].lower())

    counter = Counter(words)
    most_common_noun = counter.most_common()
    most_common_noun = list(filter(lambda c: len(c[0]) >= 2, most_common_noun))
    most_common_noun = list(filter(lambda c: c[0] not in stopKeywordList, most_common_noun))
    most_common_noun = list(filter(lambda c: c[1] >= 5, most_common_noun))
    keyword_bog = pd.DataFrame(most_common_noun, columns=['keyword', 'count'])
    keyword_bog.to_excel(f"{str(dir)}/results/buzz/{keyword}_{loc}_{since}_{until}.xlsx")
    return dict(most_common_noun),len_df

keyword = 'home battery'

## california : 36.778259, -119.417931
## los angles : 34.052235, -118.243683
## san francisco : 37.773972, -122.431297

coordA = '37.09024, -95.712891'
coordB = '37.09024, -95.712891'

locA = 'usa'
locB = 'usa'


sinceA = '2020-01-01'
untilA = '2021-01-31'

sinceB = '2014-01-01'
untilB = '2019-12-31'

dict_wordA,len_df_A = analyaze_tweets(keyword,locA,sinceA,untilA,coordA)
dict_wordB,len_df_B = analyaze_tweets(keyword,locB,sinceB,untilB,coordB)
sc = setCalc(dict_wordA, dict_wordB)

interdict = sc.getInter()
differa = sc.getDiff1()
differb = sc.getDiff2()

# wordcloud 객체 생성
wcA_B, _ = draw_to_imshow(differa, palette=None, maskPic='mask_A_B.png')
wcB_A, _ = draw_to_imshow(differb, palette=None, maskPic='mask_B_A.png')
wc_inter, _ = draw_to_imshow(interdict, palette=None, maskPic='mask_inter.png')

plt.figure(5, figsize=(16, 12))
plt.imshow(wcA_B, interpolation='bilinear')
plt.imshow(wcB_A, interpolation='bilinear')
plt.imshow(wc_inter, interpolation='bilinear')
plt.axis('off'), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
plt.savefig(f"{str(dir)}/results/wordcloud/{keyword}_{locA}_{sinceA}_{untilA}_{len_df_A}_inter_{keyword}_{locB}_{sinceB}_{untilB}_{len_df_B}.png")