from almaden import Sql
import kss
import pandas as pd
from .cleanser import cleanse_text, cleanse_sentence
from tqdm import tqdm, trange

from setting import DBSetting

class Data :
    def __init__(self, dbName):
        self.db = Sql(dbName)
        self.df = pd.DataFrame()

    def get_df(self, *colnames, by_sentence_textColname = None):
        '''

        :param colnames: 행이름 str
        :param by_sentence_textColname: 문장 분해 대상 text 행이름
        :return: DataFrame
        '''
        df_documents = self.df.loc[:,list(colnames)]
        if by_sentence_textColname :
            df_sentences = pd.DataFrame()
            nrows = df_documents.shape[0]
            for i in tqdm(range(nrows),"loader : Getting Sentences ") :
                row = df_documents.iloc[i]
                text = row[by_sentence_textColname]
                if len(text) > 0 :
                    text = cleanse_text(text)
                    sentences = kss.split_sentences(text)    #텍스트 길이 300 넘는게 허다하게 나옴... 체크 필요함
                    for s in sentences :
                        s = cleanse_sentence(s)
                        if len(s) > 0 :
                            row_temp = row.copy()
                            row_temp[by_sentence_textColname] = s
                            df_sentences = df_sentences.append(row_temp)
                else :
                    continue
            print(f"loader : Getting DataFrame Done {nrows} Documents to {df_sentences.shape[0]} Sentences")
            return df_sentences
        else :
            return df_documents

    def _getSentence_(self, text_seq):
        if replace :

    def addData(self, channel, keyword, fromDate, toDate,
                tablename, dbfnameChannel, dbfnameKeyword, dbfnamePostDate, drop_duplicate_by=None):
        '''
        :param channel: str
        :param keyword: str
        :param fromDate: 'yyyy-mm-dd'
        :param toDate: 'yyyy-mm-dd'
        :param tablename: str
        :param drop_duplicate_by: 중복 제거 행이름 list. e.g.['keyword', 'url']
        :return:
        '''
        nrows0 = self.df.shape[0]
        ldf = self._load_(channel, keyword, fromDate, toDate, tablename,
                          dbfnameChannel, dbfnameKeyword, dbfnamePostDate)
        print(ldf)
        nrowsldf = ldf.shape[0]

        self.df = self.df.append(ldf)
        addednRows = nrowsldf
        droppednRows = 0

        if drop_duplicate_by:
            self.df.drop_duplicates(subset=drop_duplicate_by)
            addednRows = self.df.shape[0]-nrows0
            droppednRows = nrowsldf - addednRows
        print(f'addData : added {addednRows} rows (dropped {droppednRows} rows)')

    def _load_(self, channel, keyword, fromDate, toDate, tablename,
               dbfnameChannel, dbfnameKeyword, dbfnamePostDate):
        where_str = f"{dbfnameKeyword}='{keyword}' and {dbfnameChannel}='{channel}' and {dbfnamePostDate} between '{fromDate}' and '{toDate}'"
        df = self.db.select(tablename,  "*", where_str, asDataFrame=True)
        return df

