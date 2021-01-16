from engine.analysis import kano
import pymysql
import pandas as pd
from os.path import dirname
from pathlib import Path
base = str(Path.cwd())

conn = pymysql.connect(host='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                       user='datacast', password='radioga12!', charset='utf8mb4',db='dalmaden')
curs = conn.cursor(pymysql.cursors.DictCursor)
#
# fromdates=['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01',
#           '2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01']
# todates = ['2020-12-31','2019-12-31','2018-12-31','2017-12-31','2016-12-31','2015-12-31','2014-12-31','2013-12-31','2012-12-31','2011-12-31',
#           '2010-12-31','2009-12-31','2008-12-31','2007-12-31','2006-12-31','2005-12-31','2004-12-31','2003-12-31']
# publishtimes = ['2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003']
fromdates = ['0000-00-00']
todates = ['0000-00-00']
publishtimes =['2020']
for fromdate,todate,publishtime in zip (fromdates,todates,publishtimes):
    sql_select_sentiment_analyze = 'select kt.id as id,kt.name as name,kt.product_category as product_category,kc.category1 as label,CAST(sum(pos) as INT) as nPos,CAST(sum(neg) as INT) as nNeg,' \
                                   'YEAR(sd.post_date) as publishtime from sdata as sd join kano_category as kc on sd.cate_id=kc.id join kano_task as kt on kc.kano_task_id=kt.id where kt.id=31 group by cate_id'
    curs.execute(sql_select_sentiment_analyze)
    rows = curs.fetchall()
    df_sentiment_analyze = pd.DataFrame(rows)


    df_sentiment_analyze_extracted_column = df_sentiment_analyze.copy().loc[:,['id','name','product_category','label','nPos','nNeg']]
    kano_df = kano.get_df_kano(df_sentiment_analyze_extracted_column)
    kano_df['publishtime'] = publishtime
    kano_df['channel']= 'navernews'
    kano_df.to_csv('{}/_{}_{}_by_category.csv'.format(base,'kano', 'scatter'), mode='a')
    # df_sentiment_analyze_extracted_column = df_sentiment_analyze.copy().loc[:,['id','name','product_category','channel','fromdate','todate','label','sentence','pos','neg']]
    # df_sentiment_analyze_extracted_column = df_sentiment_analyze_extracted_column.groupby(by=["id","name","product_category",'channel','fromdate','todate',"label"], as_index=False).sum()
    # df_sentiment_analyze_extracted_column = df_sentiment_analyze_extracted_column.rename(columns={'pos':'nPos','neg':'nNeg'})
    print(df_sentiment_analyze_extracted_column)