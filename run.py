import dafunctions as da

df = da.load_df('naverblog','은평구','2019-01-01','2020-06-30')
bow = da.get_df_bow(df['text'])
da.write_csv(df, 'test.csv')
