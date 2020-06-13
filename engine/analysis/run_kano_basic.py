from engine.analysis import kano
from engine.preprocess import loader
import pandas as pd
from almaden import *

xy_path = 'C:/Users/kjy/Program/DAlmaden/position/kano'
img_path = 'C:/Users/kjy/Program/DAlmaden/img/kano'

keyword = 'ICL 렌즈삽입술'
channel = 'Naver Blog'
fromdate = '2017-01-01'
todate = '2020-05-31'
d = Sql('sociallistening')

da = d.select('tasksent',what='category,sub_keyword, pos_num,neg_num,startdate',
              where="keyword='{}' and startdate='{}' and enddate='{}' and date(accesstime)='2020-06-12'".format(keyword, fromdate, todate),
              asDataFrame=True)

da.rename(columns={'category':'label', 'pos_num':'nPos','neg_num':'nNeg'}, inplace=True)
kano_da = da.loc[:,[
    'label', 'sub_keyword','nPos', 'nNeg','startdate'
                   ]]

kano_da = kano.get_df_kano(kano_da)
kano_da.to_csv('{}/{}_{}_{}_{}.csv'.format(xy_path,keyword, channel,'2017-01-01', '2020-12-31'), mode='a')
img_path = '{}/{}_{}_{}_{}'.format(img_path,keyword, channel, fromdate, todate)
plt = kano.visualize_df_kano(kano_da,img_path)



# keyword = 'ICL 렌즈삽입술'
# channel = 'Naver Blog'
# fromdate = '2017-01-01'
# todate = '2020-05-31'
#
#
# df_2020 = loader._load_(channel, keyword, fromdate, todate, 'tasksent')
#
#
# print(df_2020)
# df_total = df_2020.loc[:,['category','pos_num','neg_num']].copy()
#
# df_total.rename(columns={'category':'label', 'pos_num':'nPos','neg_num':'nNeg'}, inplace=True)
# kano_df = df_total.loc[:,[
#     'label', 'nPos', 'nNeg'
#                    ]]
#
# kano_df = kano.get_df_kano(kano_df)
# kano_df.loc[:,'publishtime'] = fromdate
# kano_df.loc[:,'subkey'] = df_2020['sub_keyword']
#
# kano_df = kano.get_df_kano(kano_df)
#
# kano_df.to_csv('{}/{}_{}_{}_{}.csv'.format(xy_path,keyword, channel,'2017-01-01', '2020-12-31'), mode='a')
# print(kano_df)
# img_path = '{}/{}_{}_{}_{}'.format(img_path,keyword, channel, fromdate, todate)
# kano.visualize_df_kano(kano_df,img_path)
