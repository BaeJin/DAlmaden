import pymysql

conn = pymysql.connect(host='106.246.169.202',db='dalmaden', user='root', password='robot369')
curs = conn.cursor(pymysql.cursors.DictCursor)
keyword = '향수'
fromdate = '2019-01-01'
todate = '2020-06-01'
sql_select = "select * from cdata where keyword=\'%s\' and post_date between \'%s\' and \'%s\'"%(keyword, fromdate,todate)
# sql = 'SELECT * FROM kano_task AS kt JOIN kano_category AS kc ON kt.id=kc.kano_task_id JOIN cate_keyword AS ck ON kc.id=ck.cate_id WHERE kt.id=3'
curs.execute(sql_select)
rows = curs.fetchall()
for row in rows:
    print(row)