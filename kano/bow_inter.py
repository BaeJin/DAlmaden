from kano.engine import socialListening
import pandas as pd

#keyword , channel 설정하기
keywords_set_A = {'keyword': '전라도 김치', 'fromdate': '2010-01-01', 'todate': '2020-06-30', 'channel': 'naverblog'}
keywords_set_B = {'keyword': '경상도 김치', 'fromdate': '2010-01-01', 'todate': '2020-06-30', 'channel': 'naverblog'}

keywordA = keywords_set_A['keyword']
type = 'blog'
channel = keywords_set_A['channel']
lang = 'korean'
fromdate = keywords_set_A['fromdate']
todate = keywords_set_A['todate']
nurl = 2000
mb = socialListening.Makebow(keywordA, type, channel, lang, pos=None, fromdate= fromdate, todate = todate, nurl=nurl)
_,dict_word_A = mb.get_bow()

keywordB = keywords_set_B['keyword']
type = 'blog'
channel = keywords_set_B['channel']
lang = 'korean'
fromdate = keywords_set_B['fromdate']
todate = keywords_set_B['todate']
nurl = 2000
mb = socialListening.Makebow(keywordB, type, channel, lang, pos=None, fromdate= fromdate, todate = todate, nurl=nurl)
_,dict_word_B = mb.get_bow()

samekeys = dict_word_A.keys() & dict_word_B.keys()
intersect = {}
print(samekeys)
kyo_list = []
for k in samekeys:
    v = min(dict_word_A[k],dict_word_B[k])
    kyo_dict = {'keyword': k ,'count':v}
    kyo_list.append(kyo_dict)
df_inter = pd.DataFrame(kyo_list,columns=['keyword','count'])
print(df_inter)
df_inter.to_excel('{}_inter_{}.xlsx'.format(keywordA,keywordB),encoding='utf-8',engine='xlsxwriter')