import dafunctions as da

df = da.load_df('naverblog','라식','2015-01-01','2020-06-30',by_sentence_textColname='text')
df_bow = da.get_df_bow(df['text'], channel = 'naverblog', duplicate_count=False)
da.write_csv(df, 'test.csv')



df_sent = da.load_df('naverblog','마스크','2010-01-01','2020-12-31',by_sentence_textColname='text',
             colNames=["id", "channel", "keyword", "publishtime", "content", "url"],
             dbName='sociallistening', tablename='sent')