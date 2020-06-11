from engine.analysis import kano
from engine.preprocess import loader
import pandas as pd

loader=loader.Data('sociallistening')

keyword = '마스크'
channel = 'Naver Blog'
fromdate = '2015-01-01'
todate = '2018-12-31'
xy_path = 'C:/Users/kjy/Program/DAlmaden/position/kano'
img_path = 'C:/Users/kjy/Program/DAlmaden/img/kano'
df_2015 = loader._load_(channel, keyword, '2015-01-01', '2015-12-31', 'tasksent')
df_2016 = loader._load_(channel, keyword, '2016-01-01', '2016-12-31', 'tasksent')
df_2017 = loader._load_(channel, keyword, '2017-01-01', '2017-12-31', 'tasksent')
df_2018 = loader._load_(channel, keyword, '2018-01-01', '2018-12-31', 'tasksent')

df_2019 = loader._load_(channel, keyword, '2018-01-01', '2018-12-31', 'tasksent')
df_2020 = loader._load_(channel, keyword, '2018-01-01', '2018-12-31', 'tasksent')

df = pd.DataFrame
df_total = pd.DataFrame

df_total = df_2015.loc[:,['category','pos_num','neg_num']].copy()
df_total['pos_num'] = df_2015['pos_num']+ df_2016['pos_num'] + df_2017['pos_num'] + df_2018['pos_num']
df_total['neg_num'] = df_2015['neg_num']+ df_2016['neg_num'] + df_2017['neg_num'] + df_2018['neg_num']

df_total_2 = df_2019.loc[:,['category','pos_num','neg_num']].copy()
df_total_2['pos_num'] = df_2019['pos_num']+ df_2020['pos_num']
df_total_2['neg_num'] = df_2019['neg_num']+ df_2020['neg_num']


df_total.rename(columns={'category':'label', 'pos_num':'nPos','neg_num':'nNeg'}, inplace=True)
kano_df = df_total.loc[:,[
    'label', 'nPos', 'nNeg'
                   ]]
df_total_2.rename(columns={'category':'label', 'pos_num':'nPos','neg_num':'nNeg'}, inplace=True)
kano_df_2 = df_total_2.loc[:,[
    'label', 'nPos', 'nNeg'
                   ]]
kano_df = kano.get_df_kano(kano_df)
print(kano_df)
kano_df.loc[:,'publishtime'] = '2015-01-01'
print(kano_df)

kano_df['subkey'] = df_2015['sub_keyword']
print(kano_df)

kano_df_2 = kano.get_df_kano(kano_df_2)
kano_df_2.loc[:,'publishtime'] = '2020-01-01'
kano_df_2.loc[:,'subkey'] = df_2015['sub_keyword']

kano_df_3 = pd.concat([kano_df,kano_df_2])

print(kano_df_3)
kano_df_3.to_csv('{}/{}_{}_{}_{}.csv'.format(xy_path,keyword, channel, fromdate, todate))
# print(kano_df)
# img_path = '{}/{}_{}_{}_{}'.format(img_path,keyword, channel, fromdate, todate)
# plt = kano.visualize_df_kano(kano_df,img_path)
