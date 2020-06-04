from konlpy.tag import Kkma
import pandas as pd
import pymysql
import re
import json
from collections import OrderedDict
from datetime import datetime
import pandas as pd
import os
import sys

def tagConvert(t):
    t = t.replace('/EPH;', '/EP;')
    t = t.replace('/EPT;', '/EP;')
    t = t.replace('/EPP;', '/EP;')
    t = t.replace('/EFN;', '/EF;')
    t = t.replace('/EFQ;', '/EF;')
    t = t.replace('/EFO;', '/EF;')
    t = t.replace('/EFA;', '/EF;')
    t = t.replace('/EFI;', '/EF;')
    t = t.replace('/EFR;', '/EF;')
    t = t.replace('/ECE;', '/EC;')
    t = t.replace('/ECD;', '/EC;')
    t = t.replace('/ECS;', '/EC;')
    t = t.replace('/VXV;', '/VX;')
    t = t.replace('/VXA;', '/VX;')
    t = t.replace('/ETD;', '/ETM;')
    t = t.replace('/MDT;', '/MM;')
    t = t.replace('/MDN;', '/MM;')
    t = t.replace('/MD;', '/MM;')
    t = t.replace('/NNM;', '/NNB;')
    return t


os.system('')
# sentiment_intensities = pd.read_csv("intensity.csv")

sentiment_words = pd.read_csv("polarity.csv")
##print(len(sentiment_words))
##for i in range(len(sentiment_words)):
##    print(sentiment_words.iloc[i,0])
##
##
##exit()


sstime = datetime.now()
nlp = Kkma()
keyword = '호텔'

category = "교통"
subj_str = "버스,터미널,교통,역,택시"

channel = "Booking.com"

quantity = 1

subj_list = subj_str.split(",")

conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                       db='crawl2', charset='utf8mb4')
# 106.246.169.202
# 192.168.0.105
curs = conn.cursor(pymysql.cursors.DictCursor)
sql = "select * from scrapying where (keyword=\'%s\') and channel=\'%s\'" % \
      (keyword, channel)
curs.execute(sql)
rows = curs.fetchall()
text = ''
print(keyword, len(rows))
for i, row in enumerate(rows):
    text += row['review']
conn.close()
# print('\n\ntext=',text)

# subj = '직원'
pcheck_list = []
pcheck_dict = {}
subjScore = 0
subjCount = 0
subjNegScore = 0
subjNegCount = 0
subjPosScore = 0
subjPosCount = 0
v = 0
sentenceList = text.split('.')
try:
    for sentence in sentenceList:
        sentence = sentence.replace('.', ' ')
        words = sentence.split(' ')
        phraseList = []
        for subj in subj_list:
            for wi, word in enumerate(words):
                if subj in word:
                    phrase = ''
                    for pidx in range(wi - 2, wi + 8):
                        # print(pidx, len(words))
                        if pidx < 0: continue
                        if pidx >= len(words): continue
                        phrase += words[pidx] + ' '
                    phraseList.append(phrase)

        for phrase in phraseList:
            subjCount += 1
           #if v % 1 == 0: print('\n\n', phrase)
            try:
                result = nlp.pos(phrase)
            except Exception as e:
                print(e)
            # print('\nresult=',result)

            res = ';'
            for r in result:
                res += r[0] + "/" + r[1] + ";"
            res = tagConvert(res)
            # print(res)
            sumScore = 0
            for i in reversed(range(len(sentiment_words))):
                ngram = sentiment_words.iloc[i, 0]
                ngStr = re.sub('/[A-Z]+;', '', ngram + ';')
                # ngStr = ngStr[1:]

                k = res.count(ngram)
                if k > 0:
                    score = k * (sentiment_words.iloc[i, 6] - sentiment_words.iloc[i, 3])
                    sumScore += score
                    subjScore += score
                    # print(ngram, " : ", k, sentiment_words.iloc[i, 6] - sentiment_words.iloc[i, 3], score)
                    # if score > 0:
                    #     res = res.replace(ngram, u'\u001b[42;1m' + ngStr + u'\u001b[40m')
                    # elif score < 0:
                    #     res = res.replace(ngram, u'\u001b[41;1m' + ngStr + u'\u001b[40m')
                    # else:
                    #     res = res.replace(ngram, u'\u001b[43;1m' + ngStr + u'\u001b[40m')

            # res = re.sub('/[A-Z]+;', '', res)
            # if v % 1 == 0: print(res)
            # if v % 1 == 0: print("Phrase score = ", sumScore)
            pcheck_dict = {'phrase': res,'sentiment': 'POS' if sumScore>0 else 'NEG', 'point': sumScore }
            pcheck_list.append(pcheck_dict)
            if sumScore > 0:
                subjPosScore += score
                subjPosCount += 1
            elif sumScore < 0:
                subjNegScore += score
                subjNegCount += 1

            v += 1
            print(v, category)
        # if v>300: break
    pos_rate = str(round((subjPosCount / (subjPosCount + subjNegCount)) * 100, 2)) + '%'
    neg_rate = str(round((subjNegCount / (subjPosCount + subjNegCount)) * 100, 2)) + '%'

    print("Subject %s count = %d, score = %d, average = %5.2f" % (category, subjCount, subjScore, (subjScore / subjCount)))
    print("Positive count = %d, score = %d, average = %5.2f" % (subjPosCount, subjPosScore, (subjPosScore / subjPosCount)))
    print("Negative count = %d, score = %d, average = %5.2f" % (subjNegCount, subjNegScore, (subjNegScore / subjNegCount)))
    print("Pos:Neg = %5.2f:%5.2f" % (subjPosCount / (subjPosCount + subjNegCount), subjNegCount / (subjPosCount + subjNegCount)))
except:
    print("error")
try:
    ratio_dict = {'pos': subjPosCount , 'neg': subjNegCount, 'pos_rate': str(round((subjNegCount/(subjPosCount + subjNegCount))*100,2))+'%', 'neg_rate': str(round((subjNegCount/(subjPosCount + subjNegCount))*100,2))+'%'}
except :
    print('division error')

pd_rate = pd.DataFrame(ratio_dict, index=[0])

pd_rate.to_excel("pol/rate/pol_rate_"+keyword+"_"+channel+".xlsx", encoding="utf-8", index=True)

pd_phrase = pd.DataFrame(pcheck_list, columns = ('phrase','sentiment','point'))
pd_phrase.to_excel("pol/phrase/pol_phrase_"+keyword+"_"+subj_str+"_"+channel+".xlsx", encoding="utf-8", index=True)

fftime = datetime.now() - sstime
try:
    pd_time = pd.read_csv("pol/time/analyze_pol_time.csv")
except Exception as e:
    time_dict = {'keyword': keyword, 'quantity': quantity, 'time': fftime}
    df_time = pd.DataFrame(time_dict, columns=('keyword', 'quantity', 'time'), index=[0])
    df_time.to_csv("pol/time/analyze_pol_time.csv", mode="a", index=True, header=False, encoding='euc-kr')

conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                       db='crawl', charset='utf8mb4')
curs = conn.cursor(pymysql.cursors.DictCursor)

sql = "insert into pol_rate(keyword, category, sub_keyword ,channel, fun_count , pos_num, neg_num, pos_rate, neg_rate, crawltime)"\
+ "values (\'%s\',\'%s\' ,\'%s\', \'%s\', \'%d\',\'%d\', \'%d\', \'%s\', \'%s\', \'%s\')" % \
(keyword, category,subj_str, channel, subjCount, subjPosCount, subjNegCount, pos_rate, neg_rate, fftime)
curs.execute(sql)
conn.commit()
conn.close()
