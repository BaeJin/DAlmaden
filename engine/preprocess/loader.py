from almaden import Sql
import kss

class Data :
    def __init__(self, dbName='dalmaden'):
        self.db = Sql(dbName)
        self.df = None

    def _load_(self, channel, keyword, fromDate, toDate, tablename='cdata'):
        where_str = f"keyword='{keyword}' and channel='{channel}' and post_date between '{fromDate}' and '{toDate}'"
        ldf = self.db.select(tablename,  "*", where_str, asDataFrame=True)
        return ldf

    def addData(self, channel, keyword, fromDate, toDate,
                tablename='cdata', unique = True, drop_by=['keyword','url']):
        ldf = self._load_(channel, keyword, fromDate, toDate, tablename)
        print(ldf)
        if self.df is None :
            self.df = ldf
            nrow1 = self.df.shape[0]
            nrow2 = nrow1
            if unique:
                self.drop_duplicates(subset=drop_by)
                nrow2 = self.df.shape[0]
            print(f'addData : added {nrow2} rows (dropped {nrow1 - nrow2} rows)')
        else :
            nrow0 = self.df.shape[0]
            self.df = self.df.append(ldf)
            nrow1 = self.df.shape[0]
            nrow2 = nrow1
            if unique:
                self.drop_duplicates(subset=drop_by)
                nrow2 = self.df.shape[0]
            print(f'addData : added {nrow2-nrow0} rows (dropped {nrow1-nrow2} rows)')

    def _textToSentences_(self, text) :
        kss.split_sentences(text)



    def drop_duplicates(self,subset=None):
        self.df = self.df.drop_duplicates(subset=subset)

    def shape(self):
        return self.df.shape





data = Data('dalmaden')
data.addData('naverblog','복숭아','2020-03-20','2020-05-15',unique=True,drop_by=['keyword','url'])
data.df.text



import pandas as pd
df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))

df2 = pd.DataFrame([[3, 4], [3, 4]], columns=list('AB'))
a = df.append(df2)
a.drop_duplicates()

db = Sql('dalmaden')
def _load_(channel, keyword, fromDate, toDate, tablename='cdata'):
    where_str = f"keyword='{keyword}' and channel='{channel}' and post_date between '{fromDate}' and '{toDate}'"
    ldf = db.select(tablename, "*", where_str, asDataFrame=True)
    return ldf

df1 = _load_('naverblog','복숭아','2020-03-20','2020-05-15')
df2 = _load_('naverblog','복숭아','2020-03-20','2020-05-15')
