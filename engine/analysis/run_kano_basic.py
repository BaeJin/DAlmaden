from engine.analysis import kano
from engine.preprocess import loader
import pandas as pd

loader=loader.Data('sociallistening')

keyword = '마스크'
channel = 'Naver Blog'
fromdate = '2019-01-01'
todate = '2019-12-31'
xy_path = 'C:/Users/kjy/Program/DAlmaden/position/kano'
img_path = 'C:/Users/kjy/Program/DAlmaden/img/kano'
df_2020 = loader._load_(channel, keyword, '2019-01-01', '2019-12-31', 'tasksent')

df = pd.DataFrame
df_total = pd.DataFrame

df_total = df_2020.loc[:,['category','pos_num','neg_num']].copy()

df_total.rename(columns={'category':'label', 'pos_num':'nPos','neg_num':'nNeg'}, inplace=True)
kano_df = df_total.loc[:,[
    'label', 'nPos', 'nNeg'
                   ]]

kano_df = kano.get_df_kano(kano_df)
kano_df.loc[:,'publishtime'] = '2019-01-01'
kano_df.loc[:,'subkey'] = df_2020['sub_keyword']

kano_df = kano.get_df_kano(kano_df)

kano_df.to_csv('{}/{}_{}_{}_{}.csv'.format(xy_path,keyword, channel,'2015-01-01', '2018-12-31'), mode='a')
print(kano_df)
img_path = '{}/{}_{}_{}_{}'.format(img_path,keyword, channel, fromdate, todate)
plt = kano.visualize_df_kano(kano_df,img_path)

