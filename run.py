import dafunctions as da

df = da.get_df('naverblog','복숭아','2020-05-01','2020-06-30', with_text_sentence=True)

# df_bow = da.get_df_bow(df['text'], channel = 'naverblog', duplicate_count=False)
# da.write_csv(df, 'test.csv')

#
# df_sent = da.load_df('naverblog','마스크','2010-01-01','2020-12-31',by_sentence_textColname='text',
#              colNames=["id", "channel", "keyword", "publishtime", "content", "url"],
#              dbName='sociallistening', tablename='sent')