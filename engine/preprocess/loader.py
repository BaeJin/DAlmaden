from almadenkorea.db import Sql
import kss
import pandas as pd
from .cleanser import cleanse_text, cleanse_sentence
from tqdm import tqdm, trange

class TextDataLoader :
    def __init__(self, tableName, dbName, hostIP, port, userID, password, charset='utf8mb4'):
        self.tableName = tableName
        self.db = Sql(dbName=dbName,
                      hostIP=hostIP,
                      port=port,
                      userID=userID,
                      password=password,
                      charset=charset)
        self.text_fieldName = 'text'
        self.duplicateCheck_filedNames = ['id']
        self.fiendNames = []
        self.df = None

    def addData(self, **params):
        channel_fieldName = 'channel'
        keyword_fieldName = 'keyword'
        date_fieldName = 'date'
        text_fieldName = 'text'

    def set_duplicateCheck_fieldName(self, duplicateChecker_list):
        self.duplicateCheck_filedNames = duplicateChecker_list

    def get_df(self):
        return self.df

    def mutate_sentence(self):
        '''
        :param colnames: 행이름 str
        :param by_sentence_textColname: 문장 분해 대상 text 행이름
        :return: DataFrame
        '''
        df_new = pd.DataFrame()
        nrows = self.df.shape[0]
        for i in tqdm(range(nrows),"loader : Getting Sentences ") :
            row = self.df.iloc[i]
            text = row[self.text_fieldName]
            if len(text) > 0 :
                text = cleanse_text(text)
                sentences = kss.split_sentences(text)    #텍스트 길이 300 넘는게 허다하게 나옴... 체크 필요함
                for s in sentences :
                    s = cleanse_sentence(s)
                    if len(s) > 0 :
                        row_temp = row.copy()
                        row_temp['text_sentence'] = s
                        df_new = df_new.append(row_temp)
            else :
                continue
        print(f"loader : Getting DataFrame Done {nrows} Documents to {df_new.shape[0]} Sentences")
        self.df = df_new

    def addData_where(self, where_str, drop_duplicate):

        nrows0 = self.df.shape[0]

        ldf = self.db.select(self.tableName, ", ".join(self.fieldNames), where_str, asDataFrame=True)
        print(ldf)
        nrowsldf = ldf.shape[0]

        self.df = self.df.append(ldf)
        addednRows = nrowsldf
        droppednRows = 0

        if drop_duplicate:
            self.df.drop_duplicates(subset=self.duplicateChecker_fieldNames)
            addednRows = self.df.shape[0] - nrows0
            droppednRows = nrowsldf - addednRows
        print(f'addData : added {addednRows} rows (dropped {droppednRows} rows)')

    def addData(self, channel, keyword, fromDate, toDate, drop_duplicate):
        where_str = f"{self.keyword_fieldName}='{keyword}' and {self.channel_fieldName}='{channel}' and {self.date_fieldName} between '{fromDate}' and '{toDate}'"
        self.addData_where(where_str, drop_duplicate)


