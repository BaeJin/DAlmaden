from almaden import Sql
import kss
import pandas as pd
from .cleanser import cleanse_text, cleanse_sentence

class Data :
    def __init__(self, dbName):
        self.db = Sql(dbName)
        self.df = pd.DataFrame()

    def _load_(self, channel, keyword, fromDate, toDate, tablename):

        # where_str = f"keyword='{keyword}' and channel='{channel}' and post_date between '{fromDate}' and '{toDate}'"
        where_str = f"keyword='{keyword}' and channel='{channel}' and startdate='{fromDate}' and enddate='{toDate}'"

        ldf = self.db.select(tablename,  "*", where_str, asDataFrame=True)
        return ldf

    def addData(self, channel, keyword, fromDate, toDate,
                tablename, drop_duplicate_by=None):
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
        ldf = self._load_(channel, keyword, fromDate, toDate, tablename)
        print(ldf)
        nrowsldf = ldf.shape[0]

        self.df = self.df.append(ldf)
        addednRows = nrowsldf
        droppednRows = 0

        if drop_duplicate_by:
            self.drop_duplicates(subset=drop_duplicate_by)
            addednRows = self.df.shape[0]-nrows0
            droppednRows = nrowsldf - addednRows
        print(f'addData : added {addednRows} rows (dropped {droppednRows} rows)')

    def drop_duplicates(self,subset):
        self.df = self.df.drop_duplicates(subset=subset)

    def shape(self):
        return self.df.shape

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
            for i in range(nrows) :
                if i%100 == 0 :
                    print(f"loader : Getting Sentences {i}/{nrows}")
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

