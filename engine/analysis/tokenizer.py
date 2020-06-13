from tqdm import tqdm, trange
from konlpy.tag import Okt
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from konlpy.tag import Twitter
from eunjeon import Mecab

def get_nouns_list(text_seq) :
# <<<<<<< HEAD
#     morph = Morph(nlpEngine='Mecab')
#     tokens_seq = text_seq.map(morph.get_nouns)
# =======
    morph = Morph('Okt')
    tokens_seq = map(morph.get_nouns, tqdm(text_seq), "tokenizer : Getting Tokens ")
# >>>>>>> 10d8da611b14066d083338ae2f3019981b10ea41
    return tokens_seq

def df_mutate_tokens_morph(df, textColumnName="text") :
    morph = Morph('Okt')
    df = _df_mutate_tokens_by_(df, morph.get_morphs, textColumnName, "tokens_morph")
    return df

def df_mutate_tokens_noun(df, textColumnName="text") :
    morph = Morph('Okt')
    df = _df_mutate_tokens_by_(df, morph.get_nouns, textColumnName, "tokens_noun")
    return df


def _df_mutate_tokens_by_(df, tokenizefunction, textColumnName="text", tokensColumnName="tokens") :
    rdf = df.copy()
    kwargs = {tokensColumnName : lambda dataframe : map(tokenizefunction, tqdm(dataframe[textColumnName], "tokenizer : Getting Tokens "))}
    rdf = rdf.assign(**kwargs)
    return rdf




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

    def get_morphs(self, sentence, norm=True, stem=True, join=False):
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