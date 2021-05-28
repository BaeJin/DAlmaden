import pymysql
from kano.lib.wordcloud.setCalculus import setCalc, setCalckey3
from kano.lib.wordcloud.wordcloud_recolor import Wordcloud_recolor
from kano.lib.wordcloud.draw_awarness_pie import draw_awarness_pie
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk import FreqDist
from tqdm import tqdm
import pandas as pd
from eunjeon import Mecab
import re
import os
from pathlib import Path
from sqlalchemy import create_engine
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
from engine.analysis import kano
import json
import matplotlib.patches as mpatches
import matplotlib.cm as cm
from matplotlib import colors as cols
sns.set(font_scale=1.4)
rc('font',family='NanumBarunGothic')
# rc('font', family=str(Path.cwd()) + "/source/fonts/" + "NanumBarunGothic.ttf")


class Task():
    def __init__(self,keyword=None,channel=None,lang=None,word_class=None,
                 fromdate=None, todate=None,type=None,pos=None,nurl=None,task_id=None,hashtag=None,loc=None,brand=None,ratio=None,tagged=None,kbf=None,file_name= None,batch_bool=None,filter=None,**kwargs):
        self.dir = Path.cwd()
        self.type = type
        self.keyword = keyword
        self.channel = channel
        self.lang = lang
        self.word_class = word_class
        self.fromdate = fromdate
        self.todate = todate
        self.brand = brand
        self.lang = lang
        self.nurl = nurl
        self.task_id = task_id
        self.pos = pos
        self.kano_dir = self.dir.parents[0]
        self.text_list = []
        self.hashtag = hashtag
        self.loc = loc
        self.most_common_30 = None
        self.ratio = ratio
        self.tagged = tagged
        self.kbf = kbf
        self.file_name = file_name
        self.batch_bool = batch_bool
        self.filter = filter
class SocialListeing(Task):
    def __init__(self,keyword=None,channel=None,lang=None,word_class=None,
                 fromdate=None, todate=None, type=None,pos=None,nurl=None,task_id=None,**kwargs):
        super(SocialListeing, self).__init__(keyword,channel,lang,word_class,
                 fromdate, todate, type,pos,nurl,task_id,**kwargs)

        if self.channel == "naverblog":
            self.stopKeywordList = ['드라이어','헤어드라이어','구매','머리','헤어','드라이','드라','안녕','생각','이기',self.keyword,"포스팅", "블로그", "댓글", "이웃추가", '이거', '제품', '가능', '사용','기능','부분','때문','정도','느낌']

        elif self.channel == "navernews":
            self.stopKeywordList = ["포스팅", "블로그", "댓글", "이웃추가",self.keyword]

        elif self.channel == "instagram":
            self.stopKeywordList = ['likeforlikes','insta','데일리룩','셀스타그램','sale','오오티디','ootdfashion','daily','instadaily','instagood','secla','오피',
                                    'ootd','dailylook',"셀스타그램","selfie","맞팔", "팔로우", "좋아요",
                                    "일상","행복","f4f",self.keyword,"대행","직구","그램","해외","쇼핑","구매","문의","주세요"]

        elif self.channel == "navershopping":
            self.stopKeywordList = [self.keyword, '사용','만족','구매','느낌','감사','제품','다음','생각','추천']

        elif self.lang == "english":
            self.stopKeywordList = stopwords.words('english')
        else:
            self.stopKeywordList = [self.keyword, '이거', '제품', '가능', '사용','기능','부분','때문','정도','느낌']
    # def select_task_group(self):
    #
    #     conn = pymysql.connect(host='10.96.5.179',
    #                            user='root',
    #                            password='robot369',
    #                            db='dalmaden')
    #     curs = conn.cursor(pymysql.cursors.DictCursor)
    #
    #     sql_select_task_id = "select task_id,COUNT(*) as num from cdata where task_id= ANY" \
    #                          "(select id from task_log where keyword=\'%s\' and channel=\'%s\' and startDate=\'%s\' and endDate=\'%s\')" \
    #                          "GROUP BY task_id ORDER BY num desc"\
    #                          %(self.keyword,self.channel,self.fromdate,self.todate)
    #     print(sql_select_task_id)
    #     curs.execute(sql_select_task_id)
    #     rows = curs.fetchall()
    #     task_id = rows[0]['task_id']
    #     self.task_id = task_id
    #     return task_id

    def select_task(self):

        conn = pymysql.connect(host='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                               user='datacast',
                               password='radioga12!',
                               db='dalmaden')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql_select_task_id = "select task_id,COUNT(*) as num from cdata where task_id= ANY" \
                             "(select id from task_log where keyword=\'%s\' and channel=\'%s\' and startDate=\'%s\' and endDate=\'%s\')" \
                             "GROUP BY task_id ORDER BY num desc"\
                             %(self.keyword,self.channel,self.fromdate,self.todate)
        print(sql_select_task_id)
        curs.execute(sql_select_task_id)
        rows = curs.fetchall()
        task_id = rows[0]['task_id']
        self.task_id = task_id
        return task_id

    def kano_read(self,pos):
        self.text_list=[]
        if self.type =='review':

            conn = pymysql.connect(host='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                                   user='datacast',
                                   password='radioga12!',
                                   db='salmaden')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            category = self.keyword
            sql=''
            if pos == 'pos':
                sql = "select * from review as r join product as p on r.product_id = p.id where category like \'%s\' and r.rating>=%d" % (
                '%'+category+'%', 4)
            elif pos == 'neg':
                sql = "select * from review as r join product as p on r.product_id = p.id where category like \'%s\' and r.rating<=%d" % (
                '%'+category+'%', 3)
            elif pos == 'all':
                sql = "select * from review as r join product as p on r.product_id = p.id where category like \'%s\' and r.rating>=%d" % (
                '%'+category+'%', 0)
            curs.execute(sql)
            rows = curs.fetchall()
            self.nurl = len(rows)
            print(self.nurl)
            for row in rows:
                try:
                    text = row['text']
                    text = re.sub(u"(http[^ ]*)", " ", text)
                    text = re.sub(u"@(.)*\s", " ", text)
                    text = re.sub(u"#", "", text)
                    text = re.sub(u"\\d+", " ", text)
                    text = re.sub(u"\\s+", " ", text)
                    text = re.sub("\\s+", " ", text)
                    self.text_list.append(text)
                except:
                    continue
        else:

            conn = pymysql.connect(host='61.98.230.194',
                                   user='root',
                                   password='almaden7025!',
                                   db='datacast2')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            category = self.keyword
            sql=''
            if pos == 'pos':
                sql = "select * from crawl_merged where positiveness=%d and keyword=\'%s\'"%(1,self.keyword)
            elif pos == 'neg':
                sql = "select * from crawl_merged where positiveness=%d and keyword=\'%s\'"%(0,self.keyword)
            elif pos == 'all':
                sql = "select * from crawl_merged where keyword=\'%s\'"%(self.keyword)

            curs.execute(sql)
            rows = curs.fetchall()
            self.nurl = len(rows)
            print(self.nurl)
            for row in rows:
                try:
                    text = row['text']
                    text = re.sub(u"(http[^ ]*)", " ", text)
                    text = re.sub(u"@(.)*\s", " ", text)
                    text = re.sub(u"#", "", text)
                    text = re.sub(u"\\d+", " ", text)
                    text = re.sub(u"[^가-힣A-Za-z]", " ",text)
                    text = re.sub(u"\\s+", " ", text)
                    text = re.sub("\\s+", " ", text)
                    self.text_list.append(text)
                except:
                    continue
        return self.text_list

    def read(self):
        if self.type =='sent':

            conn = pymysql.connect(host='61.98.230.194',
                                   user='root',
                                   password='almaden7025!',
                                   db='datacast2')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            sql = ''
            cs_text = None
            if self.word_class == 'nouns':
                cs_text = 'nouns'
            if self.word_class == 'adjs':
                cs_text = 'adjs'
            if self.word_class == 'verbs':
                cs_text = 'verbs'

            if self.pos=='pos' and self.batch_bool is None:
                sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM crawl_contents AS cc JOIN crawl_task AS ct ON cc.task_id=ct.task_id " \
                      "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
                      "WHERE (ct.keyword=\'%s\') and (ct.channel=\'%s\') AND cc.post_date BETWEEN \'%s\' AND \'%s\' AND cs.positiveness=%d"%\
                      (cs_text,self.keyword, self.channel,self.fromdate, self.todate, 1)

            elif self.pos=='neg' and self.batch_bool is None:
                sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM crawl_contents AS cc JOIN crawl_task AS ct ON cc.task_id=ct.task_id " \
                      "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
                      "WHERE (ct.keyword=\'%s\') and (ct.channel=\'%s\') AND cc.post_date BETWEEN \'%s\' AND \'%s\' AND cs.positiveness=%d"%\
                      (cs_text,self.keyword, self.channel,self.fromdate, self.todate, 0)

            elif self.pos == 'pos' and self.batch_bool:
                # sql = "select sentence,positiveness from analysis_brand_tmp"
                sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM request_batch AS rb " \
                      "JOIN crawl_request AS cr ON rb.batch_id=cr.batch_id " \
                      "JOIN crawl_request_task AS crt ON crt.request_id = cr.request_id " \
                      "JOIN crawl_task AS ct ON crt.task_id=ct.task_id " \
                      "join crawl_contents AS cc ON cc.task_id=ct.task_id " \
                      "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
                      "WHERE cs.positiveness=1 and (rb.batch_id=%s) AND cc.post_date BETWEEN \'%s\' AND \'%s\' and ct.channel= \'%s\'" % \
                      (cs_text,self.batch_bool,self.fromdate,self.todate,self.channel)

            elif self.pos == 'neg' and self.batch_bool:
                # sql = "select sentence,positiveness from analysis_brand_tmp"
                sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM request_batch AS rb " \
                      "JOIN crawl_request AS cr ON rb.batch_id=cr.batch_id " \
                      "JOIN crawl_request_task AS crt ON crt.request_id = cr.request_id " \
                      "JOIN crawl_task AS ct ON crt.task_id=ct.task_id " \
                      "join crawl_contents AS cc ON cc.task_id=ct.task_id " \
                      "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
                      "WHERE cs.positiveness=0 and (rb.batch_id=%s) AND cc.post_date BETWEEN \'%s\' AND \'%s\' and ct.channel= \'%s\'" % \
                      (cs_text,self.batch_bool,self.fromdate,self.todate,self.channel)

            elif self.pos == 'all' and self.filter == 0:
                sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM crawl_contents AS cc JOIN crawl_task AS ct ON cc.task_id=ct.task_id " \
                      "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
                      "WHERE (ct.keyword=\'%s\') and (ct.channel=\'%s\') AND cc.post_date BETWEEN \'%s\' AND \'%s\'"%\
                      (cs_text,self.keyword, self.channel,self.fromdate, self.todate)

            # elif self.pos == 'all' and self.filter==1:
            #     print('filtered')
            #     sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM crawl_contents AS cc JOIN crawl_task AS ct ON cc.task_id=ct.task_id " \
            #           "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
            #           "WHERE cc.text regexp '수수료|브랜드|평판|편리|신뢰|투표|친절|개설|hts|HTS|어플|앱|혜택|이벤트|우대|금리|계좌|모바일|서비스' " \
            #           "and cc.text not regexp '추천주|추천종목|리포트|목표|전체기사' and" \
            #           " (ct.keyword=\'%s\') and (ct.channel=\'%s\') AND cc.post_date BETWEEN \'%s\' AND \'%s\'"%\
            #           (cs_text,self.keyword, self.channel,self.fromdate, self.todate)
            # elif self.pos == 'all' and self.filter==0:
            #     print('filtered')
            #     sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM crawl_contents AS cc JOIN crawl_task AS ct ON cc.task_id=ct.task_id " \
            #           "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
            #           "WHERE (ct.keyword=\'%s\') and (ct.channel=\'%s\') AND cc.post_date BETWEEN \'%s\' AND \'%s\'"%\
            #           (cs_text,self.keyword, self.channel,self.fromdate, self.todate)

            elif self.pos == 'all' and self.batch_bool:
                # sql = "select sentence,positiveness from analysis_brand_tmp"
                sql = "SELECT cs.sentence_id,cs.text as sentence,%s AS text,cs.positiveness FROM request_batch AS rb " \
                      "JOIN crawl_request AS cr ON rb.batch_id=cr.batch_id " \
                      "JOIN crawl_request_task AS crt ON crt.request_id = cr.request_id " \
                      "JOIN crawl_task AS ct ON crt.task_id=ct.task_id " \
                      "join crawl_contents AS cc ON cc.task_id=ct.task_id " \
                      "JOIN crawl_sentence AS cs ON cc.contents_id=cs.contents_id " \
                      "WHERE (rb.batch_id=%s) AND cc.post_date BETWEEN \'%s\' AND \'%s\'" % \
                      (cs_text,self.batch_bool,self.fromdate,self.todate)


            curs.execute(sql)
            rows = curs.fetchall()
            self.nurl = len(rows)
            print("len(rows):",len(rows))
            print(sql)
            print("self.tagged:",self.tagged)

            # if self.filter is not None:
            #     filter_word_list = ['추천주','추천종목','리포트','목표','전체기사']
            #     includ_any_word_list = ['수수료', '브랜드', '평판', '편리', '신뢰', '투표', '친절', '개설', 'hts', 'HTS', '어플', '앱', '혜택', '이벤트', '우대', '금리','계좌', '모바일', '서비스']
            #     rows = list(filter(lambda row:
            #                        (not any(filter_word in row for filter_word in filter_word_list)) and
            #                        any(includ_any_word in row for includ_any_word in includ_any_word_list),
            #                        rows)
            #                 )
            # print("len(rows):",len(rows))

            kbf_nouns=None
            if self.kbf is not None:

                sql_select_kbf = "select * from request_analysis where analysis_id=11"
                curs.execute(sql_select_kbf)
                sql_select_kbf_rows = curs.fetchall()

                for row in sql_select_kbf_rows:
                    kbf_nouns = json.loads(row['kbf_nouns'])
                    kbf_nouns = kbf_nouns[self.kbf]

            if self.tagged is not None:
                if self.brand is not None:
                    print('tagged is not None','brand is not None')

                    if self.kbf is not None:

                        self.text_list=[json.loads(row['text']) for row in rows
                                        if any(brand in row['sentence'].lower() for brand in self.brand) and
                                        any(kbf in row['sentence'].lower() for kbf in kbf_nouns)]
                    else:
                        self.text_list = [json.loads(row['text']) for row in rows
                                          if any(brand in row['sentence'].lower() for brand in self.brand)]

                elif self.brand is None:
                    print('tagged is not None','brand is None')
                    if self.kbf is not None:
                        self.text_list = [json.loads(row['text']) for row in rows if any(kbf in row['sentence'].lower() for kbf in kbf_nouns)]
                    else:
                        self.text_list = [json.loads(row['text']) for row in rows]
            elif self.tagged is None:
                if self.brand is None:
                    print('tagged is None and brand is None')
                    for row in rows:
                        try:
                            text = row['sentence']
                            text = re.sub(u"(http[^ ]*)", " ", text)
                            text = re.sub(u"@(.)*\s", " ", text)
                            text = re.sub(u"#", "", text)
                            text = re.sub(u"\\d+", " ", text)
                            text = re.sub(u"[^가-힣A-Za-z]", " ", text)
                            text = re.sub(u"\\s+", " ", text)
                            text = re.sub("\\s+", " ", text)
                            self.text_list.append(text)
                        except:
                            continue
                    if self.kbf is not None:
                        self.text_list = [row['sentence'] for row in rows if any(kbf in row['sentence'].lower() for kbf in kbf_nouns)]
                    else:
                        self.text_list = [row['sentence'] for row in rows]
                elif self.brand is not None:
                    if self.kbf is not None:
                        self.text_list = [row['sentence'] for row in rows
                                          if any(brand in row['sentence'].lower() for brand in self.brand) and
                                          any(kbf in row['sentence'].lower() for kbf in kbf_nouns)]
                    else:
                        self.text_list = [row['sentence'] for row in rows
                                          if any(brand in row['sentence'].lower() for brand in self.brand)]

        elif self.type =='review':

            conn = pymysql.connect(host='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                                   user='datacast',
                                   password='radioga12!',
                                   db='salmaden')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            category = self.keyword
            sql = ''
            if self.pos=='pos':
                sql = "select * from review as r join product as p on r.product_id = p.id where category like \'%s\' and r.rating>=%d"%(category,4)
            elif self.pos=='neg':
                sql = "select * from review as r join product as p on r.product_id = p.id where category like \'%s\' and r.rating<=%d"%(category,3)
            elif self.pos == 'all':
                sql = "select * from review as r join product as p on r.product_id = p.id where category like \'%s\' and r.rating>=%d"%(category,0)
            curs.execute(sql)
            rows = curs.fetchall()
            self.nurl = len(rows)
            print(self.nurl)
            for row in rows:
                try:
                    text = row['text']
                    text = re.sub(u"(http[^ ]*)", " ", text)
                    text = re.sub(u"@(.)*\s", " ", text)
                    text = re.sub(u"#", "", text)
                    text = re.sub(u"\\d+", " ", text)
                    text = re.sub(u"\\s+", " ", text)
                    text = re.sub("\\s+", " ", text)
                    self.text_list.append(text)
                except:
                    continue

        elif self.type =='no_sent':

            conn = pymysql.connect(host='61.98.230.194',
                                   user='root',
                                   password='almaden7025!',
                                   db='datacast2')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            print('sql 조회')

            sql ="select * from crawl_contents where task_id = any (select task_id from crawl_task where keyword=\'%s\' and channel=\'%s\' and from_date>=\'%s\' and to_date<=\'%s\')"\
                 %(self.keyword,self.channel,self.fromdate,self.todate)
            # sql = "select * from cdata where task_id = \'%s\'" \
            #       % (self.task_id)
            print(sql)
            curs.execute(sql)

            rows = curs.fetchall()
            self.nurl = len(rows)

            for row in rows:
                self.text_list.append(row['text'])

        elif self.type =='navershopping_review':

            conn = pymysql.connect(host='61.98.230.194',
                                   user='root',
                                   password='almaden7025!',
                                   db='datacast2')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            sql = ''
            if self.pos=='pos':
                sql = f"select * from crawl_task as ct join crawl_contents as cc on ct.task_id=cc.task_id join crawl_sentence as cs on cc.contents_id=cs.contents_id where ct.keyword='{self.keyword}' and rating>=4"
            elif self.pos=='neg':
                sql = f"select * from crawl_task as ct join crawl_contents as cc on ct.task_id=cc.task_id join crawl_sentence as cs on cc.contents_id=cs.contents_id where ct.keyword='{self.keyword}' and rating<=2"
            elif self.pos == 'all':
                sql = f"select * from crawl_task as ct join crawl_contents as cc on ct.task_id=cc.task_id join crawl_sentence as cs on cc.contents_id=cs.contents_id where ct.keyword='{self.keyword}'"
            curs.execute(sql)
            rows = curs.fetchall()
            self.nurl = len(rows)
            print(self.nurl)
            for row in rows:
                try:
                    text = row['cs.text']
                    text = re.sub(u"(http[^ ]*)", " ", text)
                    text = re.sub(u"@(.)*\s", " ", text)
                    text = re.sub(u"#", "", text)
                    text = re.sub(u"\\d+", " ", text)
                    text = re.sub(u"\\s+", " ", text)
                    text = re.sub("\\s+", " ", text)
                    self.text_list.append(text)
                except:
                    continue

        elif self.type ==None:
            conn = pymysql.connect(host='61.98.230.194',
                                   user='root',
                                   password='almaden7025!',
                                   db='dalmaden')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            print('sql 조회')
            self.task_id = self.select_task()
            sql = "select * from crawl_contents where task_id = \'%s\'"\
                  %(self.task_id)
            print(sql)
            curs.execute(sql)

            rows = curs.fetchall()
            self.nurl = len(rows)

            for row in rows:
                self.text_list.append(row['text'])

        else:
            return
        print('read finish')

    def posTag(self):
        word_class_list = ['NN', 'NNS', 'NNP', 'NNPS'] if self.word_class == 'nouns' else ['JJ', 'JJR', 'JJS']

        words = []
        print("Getting Meaningful Words for " + self.keyword + "...", end="\t")
        pos = list()
        print(self.lang)
        if self.lang == 'english':
            remove_list = pos_tag(self.keyword)
            if self.tagged is None:

                for text in tqdm(self.text_list):
                    pos.extend(pos_tag(word_tokenize(text)))
                for p in pos:
                    if p[0] not in remove_list and p[1] in word_class_list:  # nltk
                        words.append(p[0])
            else:
                for text in tqdm(self.text_list):
                    words.extend(text)

        elif self.lang == 'korean':
            if self.tagged is None:
                word_class_list = ['NNP', 'NNG'] if self.word_class == 'nouns' else ['VA', 'IC']
                nlp = Mecab()
                remove_list = nlp.pos(self.keyword)
                for text in tqdm(self.text_list):
                    tagged_text = nlp.pos(text)
                    tagged_text = list(set(tagged_text))
                    pos.extend(tagged_text)

                for p in pos:
                    if p[0] not in remove_list and p[1] in word_class_list:  # 형용사,코모란, Mecab 기준임
                        words.append(p[0])
            else :

                for text in tqdm(self.text_list):
                    words.extend(text)

        return words

    def get_frequent_word(self,words):
        counter = Counter(words)

        most_common_noun = counter.most_common()
        most_common_noun = list(filter(lambda c :len(c[0])>=2,most_common_noun))
        most_common_noun = list(filter(lambda c :c[0] not in self.stopKeywordList,most_common_noun))
        most_common_noun = list(filter(lambda c :c[1]>=5, most_common_noun))
        keyword_bog = pd.DataFrame(most_common_noun, columns=['keyword', 'count'])
        #누적비율계산
        accumulated_sum_list,sum_count = self.get_accumulated_count(most_common_noun)

        for i in keyword_bog.index:
            keyword_bog._set_value(i, 'accumulate_count', round(accumulated_sum_list[i] / sum_count, 2))
        self.most_common_30 = most_common_noun[0:30]
        return keyword_bog, dict(most_common_noun)

    def get_accumulated_count(self,most_common_noun):
        sum_count = 0
        accumulated_sum_list = []
        for i in most_common_noun:
            sum_count += i[1]
            accumulated_sum_list.append(sum_count)
        return accumulated_sum_list,sum_count
    def get_kano_pos_neg_frequency(self,words,pol):
        counter = Counter(words)
        most_common_noun = counter.most_common()
        most_common_noun = list(filter(lambda c: len(c[0]) >= 2, most_common_noun))
        most_common_noun = list(filter(lambda c: c[0] not in self.stopKeywordList, most_common_noun))
        most_common_noun = list(filter(lambda c: c[1] >= 5, most_common_noun))
        keyword_bog = pd.DataFrame(most_common_noun, columns=['label',pol])
        return keyword_bog
    def get_kano(self):
        self.kano_read('pos')
        words_pos = self.posTag()
        self.kano_read('neg')
        words_neg = self.posTag()
        keyword_bog_pos = self.get_kano_pos_neg_frequency(words_pos,'nPos')
        keyword_bog_neg = self.get_kano_pos_neg_frequency(words_neg,'nNeg')
        print(keyword_bog_pos.head(10))
        print(keyword_bog_neg.head(10))
        df_OUTER_JOIN = pd.merge(keyword_bog_pos,keyword_bog_neg,left_on='label',right_on='label',how='outer')
        df_OUTER_JOIN.replace(np.NaN,0,inplace=True)
        for i in df_OUTER_JOIN.index:
            pos = df_OUTER_JOIN._get_value(i,'nPos')
            neg = df_OUTER_JOIN._get_value(i,'nNeg')
            df_OUTER_JOIN._set_value(i,'buzz',pos+neg)
        df_OUTER_JOIN.sort_values(by=['buzz'],axis=0,ascending=False,inplace=True)
        df_OUTER_JOIN['keyword'] = self.keyword
        df_sentiment_analyze_extracted_column = df_OUTER_JOIN.copy().loc[:,
                                                ['keyword','label', 'nPos', 'nNeg']]
        kano_df = kano.get_df_kano(df_sentiment_analyze_extracted_column[0:20])
        kano_df = kano_df[['keyword','label','nPos','nNeg','x','y']]
        kano_df.to_csv(str(self.kano_dir) + "/kano/results/kano_scatter/_{}_{}.csv".format('kano', 'scatter'), mode='a')


    def get_bow(self):
        self.read()
        words = self.posTag()
        keyword_bog, dict_word = self.get_frequent_word(words)
        self.keyword = self.keyword.replace(" | ","")
        self.keyword = self.keyword.replace(" ","")
        self.keyword = self.keyword.replace("'", "")
        self.keyword = self.keyword.replace('"','')

        keyword_bog.to_excel(str(self.kano_dir) + "/kano/results/buzz/{}_{}_{}_{}_{}_{}_{}_{}.xlsx".
                             format(self.file_name,self.keyword, self.fromdate,self.todate,self.channel,self.type,self.pos,self.nurl)
                             , encoding='utf-8', engine='xlsxwriter')
        print('make bow finish')
        keyword_bog.rename(columns={"keyword": "word"}, inplace=True)
        keyword_bog['task_id'] = self.task_id
        keyword_bog['keyword'] = self.keyword
        keyword_bog['fromdate'] = self.fromdate
        keyword_bog['channel'] = self.channel
        keyword_bog=keyword_bog[keyword_bog['accumulate_count']<=0.5]

        # counts_top_30 = pd.DataFrame(self.most_common_30)
        # counts_top_30.columns = ['keyword','count']
        # plt.figure(figsize=(10,8))
        # if self.pos=='neg':
        #     sns.barplot(x = 'count', y='keyword',data=counts_top_30, palette='Reds_r')
        # else:
        #     sns.barplot(x='count', y='keyword', data=counts_top_30, palette='Blues_r')
        # plt.savefig("{}/{}/{}/{}_{}_{}_{}_{}_{}_{}_bar.png".format(
        #     str(self.dir),
        #     'results',
        #     'barplot',
        #     self.file_name,
        #     self.keyword,
        #     self.channel,
        #     self.fromdate,
        #     self.todate,
        #     self.pos,
        #     self.nurl)
        #     )
        # plt.close()

        # engine = create_engine(
        #     ("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8").format
        #                        ('root',
        #                         'robot369',
        #                         '1.221.75.76',
        #                         3306,
        #                         'dalmaden'),
        #                         encoding='utf-8'
        # )
        # conn = engine.connect()
        # bow_check_duplication = self.select_task_from_bow()
        # if bow_check_duplication == 0:
        #     keyword_bog.to_sql(name='buzz',con=engine,if_exists='append',index=False)
        return keyword_bog, dict_word

class SlVizualize(Task):
    def __init__(self,tasks:list=None):
        super(SlVizualize, self).__init__()
        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks
        self.fontname = 'NanumBarunGothic.ttf'
    def get_words_pos_neg(self):
        num_of_task =len([x for x in self.tasks if isinstance(x,SocialListeing)])
        if num_of_task==1:
            ##SocialListening 객체
            task = self.tasks[0]
            task.get_kano()

    def get_awarness_pie(self):

            num_of_task = len([x for x in self.tasks if isinstance(x, SocialListeing)])
            if num_of_task == 1:
                ##SocialListening 객체
                task = self.tasks[0]
                keyword_bog, dict_word = task.get_bow()
                palette = 'tab10'
                self.draw_to_save(task, dict_word, palette=palette)

            elif num_of_task >= 2:
                ##SocialListening 객체1
                plt_info_list = []
                colors = ['royalblue','seagreen','orange','darkred','dimgrey']
                start_angle=0
                for index,task in enumerate(self.tasks):

                    start_angle += 0 if index==0 else self.tasks[index-1].ratio*360
                    draw_awarness_pie(task.ratio,start_angle=start_angle,color=colors[index],index=index)
                    keword_bog, dict_word = task.get_bow()
                    wc,mask_pic = self.draw_to_imshow(dict_word, maskPic='mask_test_{}.png'.format(index))
                    image_color = ImageColorGenerator(mask_pic)
                    plt_info_list.append({"ratio":task.ratio,"keyword":task.brand[0],"wc_dict":wc,"mask":mask_pic,"image_color":image_color,"color":cols.to_rgba(colors[index])})

                plt.figure(figsize=(12, 12))
                for plt_info in plt_info_list:
                    plt.imshow(plt_info['wc_dict'].recolor(color_func=plt_info['image_color']), interpolation='bilinear')
                patches = [mpatches.Patch(color=plt_info['color'], label="{}:{}%".format(plt_info['keyword'], plt_info['ratio']*100))
                           for plt_info in
                           plt_info_list]
                plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=30)
                plt.axis('off'), plt.xticks([]), plt.yticks([])
                plt.tight_layout()
                plt.margins(0,0)
                plt.savefig("{}/{}/{}/{}_{}_{}_{}_{}_{}_{}.png".format(
                    str(self.dir),
                    'results',
                    'wordcloud',
                    'awarenesss_pie',
                    self.tasks[0].keyword,
                    self.tasks[0].brand[0],
                    self.tasks[0].channel,
                    self.tasks[0].fromdate,
                    self.tasks[0].todate,
                    self.tasks[0].nurl
                    ),transparent=True)
                plt.close()
    def get_wordcloud_grouped_by_kbf(self):
        num_of_task =len([x for x in self.tasks if isinstance(x,SocialListeing)])
        if num_of_task==1:
            ##SocialListening 객체
            task = self.tasks[0]
            keyword_bog, dict_word = task.get_bow()
            palette = 'tab10'
            self.draw_to_save(task,dict_word,palette=palette,maskPic='mask.png')
        elif num_of_task==2:
            rc('font', family='NanumBarunGothic')

            ##SocialListening 객체1
            taskA = self.tasks[0]
            keyword_bogA, dict_wordA = taskA.get_bow()
            # posA = taskA.pos
            taskB = self.tasks[1]
            keyword_bogB, dict_wordB = taskB.get_bow()
            taskA.kbf = taskA.kbf.replace('/', '_') if taskA.kbf is not None else None

            sc = setCalc(dict_wordA, dict_wordB)
            pos_differ = sc.getDiff1_keyword_num()
            neg_differ = sc.getDiff2_keyword_num()
            neu_differ = sc.getInter_keyword_num()
            self.get_bar_plot(pos_differ,"pos",taskA)
            self.get_bar_plot(neg_differ,"neg",taskB)
            self.get_bar_plot(neu_differ,"neu",taskA,file_differentiate=f'{taskA.keyword}-{taskB.keyword}')

            interdict = sc.getInter()
            differa = sc.getDiff1()
            differb = sc.getDiff2()

            # wordcloud 객체 생성

            wcA_B, _ = self.draw_to_imshow(differa, palette=None, maskPic='mask_A_B.png')
            word_recolor_obj_A_B = Wordcloud_recolor(differa,wcA_B)
            word_recolor_A_B,_ = word_recolor_obj_A_B.recolor_kbf()

            wcB_A, _ = self.draw_to_imshow(differb, palette=None, maskPic='mask_B_A.png')
            word_recolor_obj_B_A = Wordcloud_recolor(differb, wcB_A)
            word_recolor_B_A,_ = word_recolor_obj_B_A.recolor_kbf()

            wc_inter, _ = self.draw_to_imshow(interdict, palette=None, maskPic='mask_inter.png')
            word_recolor_obj_inter = Wordcloud_recolor(interdict, wc_inter)
            word_recolor_inter,patches = word_recolor_obj_inter.recolor_kbf()

            # 교집합그림#
            plt.figure(5, figsize=(16, 12))
            plt.imshow(word_recolor_A_B, interpolation='bilinear')
            plt.imshow(word_recolor_B_A, interpolation='bilinear')
            plt.imshow(word_recolor_inter, interpolation='bilinear')
            plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=30)

            plt.axis('off'), plt.xticks([]), plt.yticks([])
            plt.tight_layout()
            # plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

            plt.savefig("{}/{}/{}/{}_{}_{}_{}_{}_{}_inter_{}_{}_{}_{}_{}.png".format(
                str(self.dir),
                'results',
                'wordcloud',
                taskA.keyword,
                taskA.brand[0] if taskA.brand is not None else None,
                taskA.kbf if taskA.kbf is not None else None,
                taskA.channel,
                taskA.fromdate,
                taskA.todate,
                taskA.nurl,
                taskB.keyword,
                taskB.channel,
                taskB.fromdate,
                taskB.todate,
                taskB.nurl)
                ,  transparent=True)

    def get_bar_plot(self,dict_differ,polarity,task,file_differentiate=None):
        dict_differ = dict(sorted(dict_differ.items(),key=lambda x:x[1],reverse=True))
        rc('font', family='NanumBarunGothic')
        dict_differ_df = pd.DataFrame(columns=['keyword','count'])
        for index,(key,value) in enumerate(dict_differ.items()):
            if index<30:
                dict_differ_df.at[index,'keyword'] = key
                dict_differ_df.at[index, 'count'] = value
        plt.figure(figsize=(16,12))
        if polarity == 'neg':
            sns.barplot(x='count', y='keyword',data=dict_differ_df, palette='Reds_r')
        elif polarity == 'pos':
            sns.barplot(x='count', y='keyword', data=dict_differ_df, palette='Blues_r')
        else:
            sns.barplot(x='count', y='keyword', data=dict_differ_df, palette='Greens_r')
        plt.tight_layout()
        if file_differentiate is not None:
            plt.savefig("{}/{}/{}/{}_{}_{}_{}_{}_bar.png".format(
                str(self.dir),
                'results',
                'barplot',
                file_differentiate,
                task.channel,
                task.fromdate,
                task.todate,
                polarity)
                )
            plt.close()

        else:
            plt.savefig("{}/{}/{}/{}_{}_{}_{}_{}_{}_{}_bar.png".format(
                str(self.dir),
                'results',
                'barplot',
                task.file_name,
                task.keyword,
                task.channel,
                task.fromdate,
                task.todate,
                polarity,
                task.nurl)
                )
            plt.close()
    def get_wordcloud(self):

        num_of_task =len([x for x in self.tasks if isinstance(x,SocialListeing)])
        if num_of_task==1:
            ##SocialListening 객체
            task = self.tasks[0]
            keyword_bog, dict_word = task.get_bow()
            palette = 'tab10'
            self.draw_to_save(task,dict_word,palette=palette,maskPic='mask.png')

        elif num_of_task==2:

            ##SocialListening 객체1
            taskA = self.tasks[0]
            keyword_bogA, dict_wordA = taskA.get_bow()
            posA = taskA.pos

            paletteA = 'Blues' if posA == 'pos' else 'Reds' if posA == 'neg' else 'Dark2'

            ##SocialListening 객체2
            taskB = self.tasks[1]
            keyword_bogB, dict_wordB = taskB.get_bow()
            posB =taskB.pos

            paletteB = 'Blues' if posB == 'pos' else 'Reds' if posB == 'neg' else 'tab10'

            taskA.kbf = taskA.kbf.replace('/', '_') if taskA.kbf is not None else None
            #교집합 차집합 구하기
            sc = setCalc(dict_wordA, dict_wordB)

            pos_differ = sc.getDiff1_keyword_num()
            neg_differ = sc.getDiff2_keyword_num()
            neu_differ = sc.getInter_keyword_num()

            self.get_bar_plot(pos_differ, posA, taskA)
            self.get_bar_plot(neg_differ, posB, taskB)
            self.get_bar_plot(neu_differ,"neu",taskA,file_differentiate=f'{taskA.keyword}-{taskB.keyword}')
            interdict = sc.getInter()
            differa = sc.getDiff1()
            differb = sc.getDiff2()


            print(dict_wordA)
            print(differa)
            print(dict_wordB)
            print(differb)
            #wordcloud 객체 생성
            wcA_B,_ = self.draw_to_imshow(differa, paletteA, maskPic='mask_A_B.png')
            wcB_A,_ = self.draw_to_imshow(differb, paletteB, maskPic='mask_B_A.png')
            wc_inter,_ = self.draw_to_imshow(interdict, 'brg' if posA=='all' else 'Greens', maskPic='mask_inter.png')

            #교집합그림#
            plt.figure(5, figsize=(16, 12))
            plt.imshow(wcA_B, interpolation='bilinear')
            plt.imshow(wcB_A, interpolation='bilinear')
            plt.imshow(wc_inter, interpolation='bilinear')
            plt.axis('off'), plt.xticks([]), plt.yticks([])
            plt.tight_layout()
            plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

            plt.savefig("{}/{}/{}/{}_{}_{}_{}_{}_{}_{}_{}_inter_{}_{}_{}_{}_{}_{}_{}.png".format(
                str(self.dir),
                'results',
                'wordcloud',
                taskA.file_name,
                taskA.keyword,
                taskA.brand[0] if taskA.brand is not None else None,
                taskA.type if taskA.type is not None else None,
                taskA.channel,
                taskA.fromdate,
                taskA.todate,
                taskA.nurl,
                taskB.keyword,
                taskB.brand[0] if taskB.brand is not None else None,
                taskA.type if taskB.type is not None else None,
                taskB.channel,
                taskB.fromdate,
                taskB.todate,
                taskB.nurl)
                ,pad_inches=0,
                dpi=100, transparent=True)
            plt.close()

        elif num_of_task==3:
            taskA = self.tasks[0]
            taskB = self.tasks[1]
            taskC = self.tasks[2]
            keyword_bogA, dict_wordA = taskA.get_bow()
            keyword_bogB, dict_wordB = taskB.get_bow()
            keyword_bogC, dict_wordC = taskC.get_bow()
            posA,posB,posC = taskA.pos, taskB.pos, taskC.pos

            paletteA = 'Blues' if posA == 'pos' else 'Reds' if posA=='neg' else 'Dark2'
            paletteB = 'Blues' if posB == 'pos' else 'Reds' if posB=='neg' else 'tab10'
            paletteC = 'Blues' if posC == 'pos' else 'Reds' if posC=='neg' else 'Dark2'
            paletteD = 'tab10' if posA == 'all' else 'Greens'
            paletteE = 'Dark2' if posA == 'all' else 'Greens'
            paletteF = 'tab10' if posA == 'all' else 'Greens'
            paletteG = 'brg' if posA == 'all' else 'Greens'

            ##교집합 차집합 구하기
            sc = setCalckey3(dict_wordA, dict_wordB, dict_wordC)
            interdictD = sc.getInterD()
            interdictE = sc.getInterE()
            interdictF = sc.getInterF()
            interdictG = sc.getInterG()
            differa = sc.getDiffA()
            differb = sc.getDiffB()
            differc = sc.getDiffC()
            # wordcloud 객체 생성
            wcA_B_C, _ = self.draw_to_imshow(differa, paletteA, maskPic='mask3_A(diff1).png')
            wcB_A_C, _ = self.draw_to_imshow(differb, paletteB, maskPic='mask3_B(diff2).png')
            wcC_A_B, _ = self.draw_to_imshow(differc, paletteC, maskPic='mask3_C(diff3).png')
            palette = 'tab10'
            self.draw_to_save(taskA, dict_wordA, palette=palette, maskPic='mask.png')
            self.draw_to_save(taskB, dict_wordB, palette=palette, maskPic='mask.png')
            self.draw_to_save(taskC, dict_wordC, palette=palette, maskPic='mask.png')

            wcD, _ = self.draw_to_imshow(interdictD, paletteD, maskPic='mask3_D(inter1).png')
            wcE, _ = self.draw_to_imshow(interdictE, paletteE, maskPic='mask3_E(inter2).png')
            wcF, _ = self.draw_to_imshow(interdictF, paletteF, maskPic='mask3_F(inter3).png')
            wcG, _ = self.draw_to_imshow(interdictG, paletteG, maskPic='mask3_G(inter4).png')

            plt.figure(figsize=(16, 12))
            plt.imshow(wcD, interpolation='bilinear')
            plt.imshow(wcE, interpolation='bilinear')
            plt.imshow(wcF, interpolation='bilinear')
            plt.imshow(wcG, interpolation='bilinear')
            plt.imshow(wcA_B_C, interpolation='bilinear')
            plt.imshow(wcB_A_C, interpolation='bilinear')
            plt.imshow(wcC_A_B, interpolation='bilinear')

            plt.axis('off'), plt.xticks([]), plt.yticks([])
            plt.tight_layout()
            plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

            plt.savefig("{}/{}/{}/{}_{}_{}_{}_{}_{}_inter_{}_{}_{}_{}_{}_inter_{}_{}_{}_{}_{}.png".format(
                str(self.dir),
                'results',
                'wordcloud',
                taskA.keyword,
                taskA.brand[0] if taskA.brand is not None else None,
                taskA.kbf if taskA.kbf is not None else None,
                taskA.channel,
                taskA.fromdate,
                taskA.todate,
                taskA.nurl,
                taskB.keyword,
                taskB.channel,
                taskB.fromdate,
                taskB.todate,
                taskB.nurl,
                taskC.keyword,
                taskC.channel,
                taskC.fromdate,
                taskC.todate,
                taskC.nurl)
                ,pad_inches=0,
                dpi=100, transparent=True)

            plt.show()
    def setMask(self, filename):
        self.maskPic = np.array(Image.open(filename))

    def draw_to_imshow(self,dict,palette=None,maskPic=None):

        if maskPic ==None:
            maskPic = np.array(Image.open(str(self.dir)+"/source/img/"+"mask.png"))
        else:
            maskPic = np.array(Image.open(str(self.dir)+"/source/img/"+maskPic))

        wordcloud = WordCloud(font_path=str(self.dir) + "/source/fonts/" + self.fontname, \
                              background_color="rgba(255,255,255,0)", mode='RGBA', \
                              max_font_size=120,\
                              min_font_size=18,\
                              mask=maskPic,\
                              width=200, height=200,\
                              colormap=palette) \
            .generate_from_frequencies(dict)

        return wordcloud,maskPic


    def draw_to_save(self,task,dict,index=None,palette=None,maskPic=None):
        if maskPic ==None:
            maskPic = np.array(Image.open(str(self.dir)+"/source/img/"+"test.png"))
        else:
            maskPic = np.array(Image.open(str(self.dir)+"/source/img/"+maskPic))

        wordcloud = WordCloud(font_path=str(self.dir) + "/source/fonts/" + self.fontname, \
                              background_color="rgba(255,255,255,0)", mode='RGBA', \
                              max_font_size=120,\
                              min_font_size=18,\
                              mask=maskPic,\
                              width=200, height=200,\
                              colormap=palette) \
            .generate_from_frequencies(dict)
        plt.figure(index, figsize=(12, 12))
        plt.imshow(wordcloud, interpolation='bilinear')

        plt.axis('off'), plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

        plt.savefig("{}/{}/{}/{}_{}__{}_{}_{}_{}.png".format(
            str(self.dir),
            'results',
            'wordcloud',
            task.keyword,
            task.kbf if task.kbf is not None else None,
            task.brand[0] if task.brand is not None else None,
            task.channel,
            task.fromdate,
            task.todate,
            task.nurl)
            , pad_inches=0,
            dpi=100, transparent=True)
        plt.close()