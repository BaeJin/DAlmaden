import re
from threading import Thread
import pymysql
from datetime import datetime
import json

class DAO:
    def __init__(self, host='1.221.75.76', port=3306, user='root', password='robot369', db='datacast2',
                 charset='utf8mb4'):
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                                    charset=charset)
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        self.close = self.conn.close

    def select_kbf(self,batch_id):
        sql_select_kbf = "select * from request_analysis where batch_id=\'%s\'" % (batch_id)
        self.curs.execute(sql_select_kbf)

        sql_select_kbf_rows = self.curs.fetchall()
        kbf_nouns=None
        for row in sql_select_kbf_rows:
            kbf_nouns = json.loads(row['kbf_nouns'])

        return kbf_nouns
