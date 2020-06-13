from engine.analysis import kano
from engine.preprocess import loader
import pandas as pd
from almaden import *

loader=loader.Data('sociallistening')
d = Sql('sociallistening')

keyword1 = '라식'
keyword2 = '라섹'
keyword3 = 'ICL 렌즈삽입술'
channel = 'Naver Blog'
fromdate = '2017-01-01'
todate = '2020-05-31'
xy_path = 'C:/Users/kjy/Program/DAlmaden/position/kano'
img_path = 'C:/Users/kjy/Program/DAlmaden/img/kano'


df_keyword1 = d.select('tasksent',what='category,sub_keyword, pos_num,neg_num,startdate',
              where="keyword='{}' and startdate='{}' and enddate='{}' and date(accesstime)='2020-06-12'".format(keyword1, fromdate, todate),
              asDataFrame=True)

df_keyword2 = d.select('tasksent',what='category,sub_keyword, pos_num,neg_num,startdate',
              where="keyword='{}' and startdate='{}' and enddate='{}' and date(accesstime)='2020-06-12'".format(keyword2, fromdate, todate),
              asDataFrame=True)

df_keyword3 = d.select('tasksent',what='category,sub_keyword, pos_num,neg_num,startdate',
              where="keyword='{}' and startdate='{}' and enddate='{}' and date(accesstime)='2020-06-12'".format(keyword3, fromdate, todate),
              asDataFrame=True)


# concat_df = pd.concat([df_keyword1,df_keyword2,df_keyword3])
#
# print(df_total)
# print(len(df_total))
# input()
df_total = df_keyword1.loc[:,['category','pos_num','neg_num']].copy()

df_total['pos_num'] = df_keyword1['pos_num']+ df_keyword2['pos_num'] + df_keyword3['pos_num']

print(df_total)

df_total['neg_num'] = df_keyword1['neg_num']+ df_keyword2['neg_num'] + df_keyword3['neg_num']

df_total.rename(columns={'category':'label', 'pos_num':'nPos','neg_num':'nNeg'}, inplace=True)
kano_df = df_total.loc[:,[
    'label', 'nPos', 'nNeg'
                   ]]
print(kano_df)

kano_df = kano.get_df_kano(kano_df)
keyname = "{}+{}+{}".format(keyword1,keyword2,keyword3)
kano_df.loc[:,'keyword'] = keyname


kano_df.to_csv('{}/{}_{}_{}_{}.csv'.format(xy_path,keyname, channel, fromdate, todate))
img_path = '{}/{}_{}_{}_{}'.format(img_path,keyname, channel, fromdate, todate)
print(img_path)
plt = kano.visualize_df_kano(kano_df,img_path)
