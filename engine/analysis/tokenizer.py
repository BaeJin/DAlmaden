import re
from collections import Counter
from konlpy.tag import Okt
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from konlpy.tag import Twitter
from MeCab import Tagger as Mecab
import MeCab

class Morph :
    def __init__(self, nlpEngine = "Mecab"):
        '''e
        원하는 형태소 분석기 엔진으로 형태소 분석기 생성
        :param nlpEngine: 형태소 분석기 이름(첫글자 대문자) str
        '''
        self.nlpEngine = nlpEngine
        if nlpEngine == "Okt":
            self.nlp = Okt()
        elif nlpEngine == "Komoran":
            self.nlp = Komoran()
        elif nlpEngine == "Kkma":
            self.nlp = Kkma()
        elif nlpEngine == "Hannanum":
            self.nlp = Hannanum()
        elif nlpEngine == "Mecab":
            self.nlp = Mecab()
        elif nlpEngine == "Twitter":
            self.nlp = Twitter()
        else:
            raise NameError("unknown nlp name")

    def tokenize(self, sentence, norm=True, stem=True, join=False):
        if self.nlpEngine == "Mecab":
            try :
                a = self.nlp.parse(sentence)
                b = [aa.split(',') for aa in a.split('\n')][:-2]
                if stem :
                    s = [[d[3],d[0].split('\t')[1]] for d in b]
                else :
                    s = [d[0].split('\t') for d in b]
                if join :
                    j = ['/'.join(ss) for ss in s]
                else :
                    j = [tuple(ss) for ss in s]
                return j
            except :
                return []
        else :
            return self.nlp.pos(sentence, norm=norm, stem=stem, join=join)

    def get_nouns(self,text):
        if self.nlpEngine == "Mecab" :
            all_tags_raw1 = self.nlp.parse(text).split("\n")
            all_tags_raw2 = [tt.split(",")[0] for tt in all_tags_raw1]
            all_tags = [t.split("\t") for t in all_tags_raw2]
            nounList = []
            for tags in all_tags :
                if len(tags) == 2 :
                    if tags[1][0:2] in ['NN','NP'] :
                        nounList.append(tags[0])
            print(nounList)
            return nounList
        else :
            return self.nlp.nouns(text)

    def get_nounCount(self, phrase):
        '''
        문장으로부터 명사 빈도 추출
        :param phrase: 문장 str
        :return: 명사 빈도 {명사:빈도,...} dict
        '''
        return dict(Counter(self.get_nounList(phrase)).most_common())

    def get_nounCounts(self, phrase_list):
        '''
        문장 리스트로부터 명사 빈도 딕셔너리의 리스트 추출
        len(phrase_list) == len(nounCounts)
        :param phrase_list: 문장 리스트 list of str
        :return: 명사 빈도 리스트[{명사:빈도,...},{명사:빈도,...}] list of dict
        '''
        nounCounts = []
        for i, phrase in enumerate(phrase_list):
            if i%100 == 0 :
                print(i)
            nounCounts.append(self.get_nounCount(phrase))
        return nounCounts

    def get_nounList_by_list(self, phrase_list):
        '''
        문장 리스트로부터 명사 리스트 추출
        :param phrase_list: 문장 리스트 list of str
        :return: 명사 리스트 list of str
        '''
        nounLists = self.get_nounLists(phrase_list)
        nounList = []
        for l in nounLists :
            nounList.extend(l)
        return nounList

    def get_nounCount_by_list(self, phrase_list):
        '''
        문장 리스트로부터 명사 빈도 추출
        :param phrase_list: 문장 리스트 list of str
        :return: 명사 빈도{명사:빈도,...} dict
        '''
        nounList = self.get_nounList_by_list(phrase_list)
        return dict(Counter(nounList).most_common())

