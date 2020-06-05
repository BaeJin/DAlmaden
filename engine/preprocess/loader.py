from almaden import Sql
import kss
import pandas as pd
from .cleanser import cleanse_text, cleanse_text_light

class Data :
    def __init__(self, dbName='dalmaden'):
        self.db = Sql(dbName)
        self.df = pd.DataFrame()
        self.dfs = None

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

    def getSentences(self, textColName = 'text'):
        df_sentences = pd.DataFrame()
        nrows = self.df.shape[0]
        for i in range(nrows) :
            if i%100 == 0 :
                print(f"loader : Getting Sentences {i}/{nrows}")
            row = self.df[i:i+1]
            row_text = row[textColName]
            if len(row_text) > 0 :
                text = row_text.to_string(index=False)
                text = cleanse_text(text)
                #print()
                #print(text)
                sentences = kss.split_sentences(text)
                for s in sentences :
                    s = cleanse_text_light(s)
                    #print("\t",s)
                    row_temp = row.copy()
                    row_temp[textColName] = s
                    df_sentences = df_sentences.append(row_temp)
            else :
                continue
        print(f"loader : Getting Sentences Done {nrows} to {df_sentences.shape[0]}")
        self.dfs = df_sentences

    def drop_duplicates(self,subset=None):
        self.df = self.df.drop_duplicates(subset=subset)

    def shape(self):
        return self.df.shape





df.shape

data = Data('dalmaden')
data.addData('naverblog','복숭아','2020-03-20','2020-05-15',unique=True,drop_by=['keyword','url'])

data.getSentences()


data.dfs

a.copy()
row= data.df[1541:1542]
row['text'].to_string(index=False)
len(a)
txt = str(a['text'])
df[1551:1552]['text']
len(a['text'])
df = data.df
data.df(1)
for i in data.df :
    print(i)
data.df=pd.DataFrame()
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
