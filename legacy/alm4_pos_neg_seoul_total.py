from konlpy.tag import Kkma
import pandas as pd
import pymysql
import re
import json
from collections import OrderedDict
from datetime import datetime
import pandas as pd
import os

class Pol_Analyzer:
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

    def __init__(self, keyword, channel, quantity, startDate, endDate):
    # sentiment_intensities = pd.read_csv("intensity.csv")

        self.sentiment_words = pd.read_csv("polarity.csv")

        self.sstime = datetime.now()
        self.nlp = Kkma()
        self.keyword = keyword
        self.channel = channel
        self.quantity = quantity

        self.startDate = startDate
        self.endDate = endDate
    def pol_anaylze(self):
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db='crawl', charset='utf8mb4')
        # 106.246.169.202
        # 192.168.0.105
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from htdocs where keyword=\'%s\' and channel=\'%s\' and publishtime>=\'%s\' and publishtime<=\'%s\' limit %d" % \
              (self.keyword, self.channel, self.startDate, self.endDate, self.quantity)
        curs.execute(sql)
        rows = curs.fetchall()
        text = ''
        print(self.keyword, len(rows))
        for i, row in enumerate(rows):
            text += row['htmltext']
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
        for sentence in sentenceList:
            sentence = sentence.replace('.', ' ')
            words = sentence.split(' ')
            phraseList = []
            for wi, word in enumerate(words):
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
                    result = self.nlp.pos(phrase)
                except Exception as e:
                    print(e)
                # print('\nresult=',result)

                res = ';'
                for r in result:
                    res += r[0] + "/" + r[1] + ";"
                res = self.tagConvert(res)
                # print(res)
                sumScore = 0
                for i in reversed(range(len(self.sentiment_words))):
                    ngram = self.sentiment_words.iloc[i, 0]
                    ngStr = re.sub('/[A-Z]+;', '', ngram + ';')
                    # ngStr = ngStr[1:]

                    k = res.count(ngram)
                    if k > 0:
                        score = k * (self.sentiment_words.iloc[i, 6] - self.sentiment_words.iloc[i, 3])
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
                print(v, self.keyword)
            # if v>300: break
        pos_rate = str(round((subjPosCount / (subjPosCount + subjNegCount)) * 100, 2)) + '%'
        neg_rate = str(round((subjNegCount / (subjPosCount + subjNegCount)) * 100, 2)) + '%'

        print("Subject %s count = %d, score = %d, average = %5.2f" % (self.keyword, subjCount, subjScore, (subjScore / subjCount)))
        print("Positive count = %d, score = %d, average = %5.2f" % (subjPosCount, subjPosScore, (subjPosScore / subjPosCount)))
        print("Negative count = %d, score = %d, average = %5.2f" % (subjNegCount, subjNegScore, (subjNegScore / subjNegCount)))
        print("Pos:Neg = %5.2f:%5.2f" % (subjPosCount / (subjPosCount + subjNegCount), subjNegCount / (subjPosCount + subjNegCount)))

        try :
            ratio_dict = {'pos': subjPosCount , 'neg': subjNegCount, 'pos_rate': str(round((subjNegCount/(subjPosCount + subjNegCount))*100,2))+'%', 'neg_rate': str(round((subjNegCount/(subjPosCount + subjNegCount))*100,2))+'%'}
        except :
            print('division error')

        pd_rate = pd.DataFrame(ratio_dict, index=[0])

        pd_rate.to_excel("pol/rate/pol_rate_"+self.keyword+"_"+self.startDate+"_"+self.endDate+".xlsx", encoding="utf-8", index=True)

        pd_phrase = pd.DataFrame(pcheck_list, columns = ('phrase','sentiment','point'))
        pd_phrase.to_excel("pol/phrase/pol_phrase_"+self.keyword+"_"+self.startDate+"_"+self.endDate+".xlsx", encoding="utf-8", index=True)

        self.fftime = datetime.now() - self.sstime
        try:
            pd_time = pd.read_csv("pol/time/analyze_pol_time.csv")
        except Exception as e:
            time_dict = {'keyword': self.keyword, 'quantity': self.quantity, 'time': self.fftime}
            df_time = pd.DataFrame(time_dict, columns=('keyword', 'quantity', 'time'), index=[0])
            df_time.to_csv("pol/time/analyze_pol_time.csv", mode="a", index=True, header=False, encoding='euc-kr')

        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db='crawl', charset='utf8mb4')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql = "insert into pol_rate(keyword, channel, fun_count , pos_num, neg_num, pos_rate, neg_rate, stdate, endate, nurl, crawltime)"\
        + "values (\'%s\',\'%s\', \'%d\',\'%d\', \'%d\', \'%s\', \'%s\', \'%s\', \'%s\', \'%d\', \'%s\')" % \
        (self.keyword, self.channel, subjCount, subjPosCount, subjNegCount, pos_rate, neg_rate, self.startDate, self.endDate, self.quantity, self.fftime)
        curs.execute(sql)
        conn.commit()
        conn.close()