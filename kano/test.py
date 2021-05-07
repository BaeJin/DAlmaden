import pymysql

conn = pymysql.connect(host='10.96.5.179',
                       user='root',
                       password='robot369',
                       db='datacast2')
curs = conn.cursor(pymysql.cursors.DictCursor)

sql = "SELECT * FROM request_batch AS rb JOIN crawl_request AS cr " \
      "ON rb.batch_id = cr.batch_id JOIN crawl_request_task AS crt " \
      "ON cr.request_id = crt.request_id JOIN crawl_task AS ct " \
      "ON ct.task_id = crt.task_id JOIN crawl_contents AS cc " \
      "ON cc.task_id = ct.task_id " \
      "WHERE rb.batch_id=102 AND cc.text LIKE '%아침%' and cr.channel ='instagram'"

curs.execute(sql)
rows = curs.fetchall()
for idx,row in enumerate(rows[0:100]):
    print(idx,row['author'],row['text'])