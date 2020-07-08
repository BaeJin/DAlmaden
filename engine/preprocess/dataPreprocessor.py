import pandas as pd
from tqdm import tqdm
from kss import split_sentences
from .engines import TextDataPreprocessorEngine as textEngine
#from nltk import tokenize

class TextDataPreprocessor :
    def __init__(self, df, colname_text='text', colname_sentence='sentence_text'):
        self.__df = df
        self.__colname_text = colname_text
        self.__colname_sentence = colname_sentence

    def cleanTexts(self) :
        self.__df[self.__colname_text] = [textEngine.cleanText(text) for text in self.__df[self.__colname_text]]

    def filterNews(self) :
        self.__df = self.__df[[textEngine.isNewsContents(text) for text in self.__df[self.__colname_text]]]

    def filterBlog(self) :
        self.__df = self.__df[[textEngine.isBlogContents(text) for text in self.__df[self.__colname_text]]]

    def splitSentences(self):
        df_new = pd.DataFrame()
        nrows = self.__df.shape[0]
        for i in tqdm(range(nrows), "loader : Getting Sentences "):
            row = self.__df.iloc[i]
            text = row[self.__colname_text]
            if len(text) > 0:
                sentences = split_sentences(text)  # 텍스트 길이 300 넘는게 허다하게 나옴... 체크 필요함
                #sentences = tokenize.sent_tokenize(text)
                for s in sentences:
                    s = textEngine._cut_sentence(s)
                    if len(s) > 0:
                        row_temp = row.copy()
                        row_temp[self.__colname_sentence] = s
                        df_new = df_new.append(row_temp)
            else:
                continue
        print(f"TextDataPreprocessor : Getting DataFrame Done {nrows} texts to {df_new.shape[0]} Sentences")
        self.__df = df_new

