from engine.analysis import kano
import pymysql
import pandas as pd
from os.path import dirname

base = dirname(__file__)
conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369', charset='utf8mb4',db='dalmaden')
curs = conn.cursor(pymysql.cursors.DictCursor)

sql_select_sentiment_analyze = 'SELECT kt.id as kt_id,kt.name,kt.product_category,kc.category1,ck.cate_id,s.keyword,CAST(SUM(pos) as INT) as nPos,CAST(SUM(neg) as INT) as nNeg FROM kano_task AS kt JOIN kano_category AS kc ON kt.id = kc.kano_task_id JOIN cate_keyword AS ck ON kc.id=ck.cate_id JOIN sdata AS s ON s.cate_id=ck.cate_id where kt.id=24 GROUP BY s.cate_id,s.keyword'
curs.execute(sql_select_sentiment_analyze)
rows = curs.fetchall()
name = rows[0]['name']
product_category = rows[0]['product_category']
channel = 'naverblog'

df_sentiment_analyze = pd.DataFrame(rows)

df_sentiment_analyze_extracted_column = df_sentiment_analyze.copy().loc[:,['kt_id','name','product_category','keyword','nPos','nNeg']]
kano_df = kano.get_df_kano(df_sentiment_analyze_extracted_column)
kano_df.to_csv('{}/_{}_{}_{}_by_keyword.csv'.format(base, channel,'kano', 'scatter'), mode='a')
print(df_sentiment_analyze_extracted_column)