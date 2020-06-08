from almaden import Sql
import kss
import pandas as pd
from .cleanser import cleanse_text, cleanse_sentence

class Data :
    def __init__(self, dbName='dalmaden'):
        self.db = Sql(dbName)
        self.df = pd.DataFrame()

    def _load_(self, channel, keyword, fromDate, toDate, tablename='cdata'):
        where_str = f"keyword='{keyword}' and channel='{channel}' and post_date between '{fromDate}' and '{toDate}'"
        ldf = self.db.select(tablename,  "*", where_str, asDataFrame=True)
        return ldf

    def addData(self, channel, keyword, fromDate, toDate,
                tablename='cdata', unique = True, drop_by=['keyword','url']):
        nrows0 = self.df.shape[0]
        ldf = self._load_(channel, keyword, fromDate, toDate, tablename)
        print(ldf)
        nrowsldf = ldf.shape[0]

        self.df = self.df.append(ldf)
        addednRows = nrowsldf
        droppednRows = 0

        if unique:
            self.drop_duplicates(subset=drop_by)
            addednRows = self.df.shape[0]-nrows0
            droppednRows = nrowsldf - addednRows
        print(f'addData : added {addednRows} rows (dropped {droppednRows} rows)')

    def drop_duplicates(self,subset=None):
        self.df = self.df.drop_duplicates(subset=subset)

    def shape(self):
        return self.df.shape

    def get_df(self, *colnames, by_sentence = ''):
        '''

        :param colnames: 행이름 str
        :param by_sentence: 문장 분해 대상 text 행이름
        :return: DataFrame
        '''
        df_documents = self.df.loc[:,list(colnames)]
        if len(by_sentence) > 0 :
            df_sentences = pd.DataFrame()
            nrows = df_documents.shape[0]
            for i in range(nrows) :
                if i%100 == 0 :
                    print(f"loader : Getting Sentences {i}/{nrows}")
                row = df_documents.iloc[i]
                text = row[by_sentence]
                if len(text) > 0 :
                    text = cleanse_text(text)
                    sentences = kss.split_sentences(text)    #텍스트 길이 300 넘는게 허다하게 나옴... 체크 필요함
                    for s in sentences :
                        s = cleanse_sentence(s)
                        if len(s) > 0 :
                            row_temp = row.copy()
                            row_temp[by_sentence] = s
                            df_sentences = df_sentences.append(row_temp)
                else :
                    continue
            print(f"loader : Getting DataFrame Done {nrows} Documents to {df_sentences.shape[0]} Sentences")
            return df_sentences
        else :
            return df_documents



data = Data('dalmaden')
data.addData('naverblog','복숭아','2020-03-20','2020-05-15',unique=True,drop_by=['keyword','url'])
df = data.get_df('post_date','text',by_sentence='text')

