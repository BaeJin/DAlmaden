import pymysql
conn = pymysql.connect(host='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                       user='datacast',
                       password='radioga12!',
                       db='dalmaden')
curs = conn.cursor(pymysql.cursors.DictCursor)




sql_select_task_id = "select task_id,COUNT(*) as num from cdata where task_id= ANY" \
                     "(select id from task_log where keyword=\'%s\' and startDate=\'%s\' and endDate=\'%s\')" \
                     "GROUP BY task_id ORDER BY num desc"%('취업준비','2017-01-01','2020-09-04')

curs.execute(sql_select_task_id)
rows = curs.fetchall()
task_id = rows[0]['task_id']
print(task_id)
print(type(task_id))