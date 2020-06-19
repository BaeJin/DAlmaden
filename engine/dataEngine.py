import pymysql
import datetime
import pandas as pd
import db_setting


class Sql :
    def __init__(self, dbName, hostIP, port ,userID, password, charset='utf8mb4'):
        self.dbName = dbName
        self.port= port
        self.hostIP = hostIP
        self.userID = userID
        self.password = password
        self.charset = charset
        self.conn = None
        self.curs = None
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.hostIP, port= self.port, user=self.userID, password=self.password,
                               db=self.dbName, charset=self.charset)
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    def query(self, query):
        self.curs.execute(query)
        self.conn.commit()
    def close(self):
        self.conn.close()

    def update_one(self,tableName, field, value, field_id, id):
        query = '''update {tableName} set {field} = {value} where {field_id}={id}'''.format(
            tableName = tableName,
            field = field,
            value=value,
            field_id = field_id,
            id=id
        )
        self.query(query)

    def select(self, tablename, what="", where="", asDataFrame=False, count=False):
        '''
        e.g. select('tablename', 'id, keyword, title', 'date like "2019%"', True)
        :param tablename: table name
        :param params: field = value or // field like %value%
        :param count:
        :return:
        '''
        if count :
            select_what = "count(*)"
        else :
            if len(what)<1 :
                select_what = "*"
            else :
                select_what = what
        sql = "select %s from %s"%(select_what, tablename)
        if len(where) > 1:
            sql+=" where "+where
        self.curs.execute(sql)
        rows = self.curs.fetchall()
        if count :
            return int(rows[0]['count(*)'])
        else :
            if asDataFrame :
                return pd.DataFrame(rows)
            else :
                return rows

    def check_duplication(self, tablename, **params):
        select_where = " and ".join([k+"="+v for k, v in params.items()])
        count = self.select(tablename, where=select_where, count=True)
        if count>0 : return True
        else : return False

    def insert_withoutDuplication(self, tablename, check_list, **params):
        '''
        e.g. insert_withoutDuplication('datatable', ['keyword','url'], keyword = 'abc', url = 'http://', date = '20150305', title = '테스트')
        :param tablename: str
        :param check_list: list
        :param params: dict
        :return: None or id(int)
        '''
        new_params = {}
        for k,v in params.items() :
            if k in check_list :
               new_params[k] = v
        if self.check_duplication(tablename, **new_params) :
            return None
        else :
            return self.insert(tablename, **params)

    def insert(self, tablename, **params):
        '''
        e.g. insert('datatable', date = '20150305', title = '테스트')
        :param tablename: str
        :param params: dict
        :return: id(int)
        '''
        '''
        :param tablename: str
        :param params: dict
        :return: id(int)
        '''
        sql = "insert into %s("%(tablename)
        sql += ",".join([str(k) for k in params.keys()])
        sql += ") values("
        sql += ",".join(["%s"]*len(params))
        sql += ")"
        vs = []
        for v in params.values() :
            if v :
                if type(v) is int or type(v) is float :
                    vs.append(v)
                else :
                    vs.append(str(v))
            else :
                vs.append(None)
        vs = tuple(vs)
        self.curs.execute(sql, vs)
        row_id = self.curs.lastrowid
        self.conn.commit()
        return row_id


    def get_now_datetime(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Table_sql :
    tableName = 'tablename'

    fieldNames = [
        'id',
        'channel',
        'keyword',
        'date'
    ]

    channel_fieldName = 'channel'
    keyword_fieldName = 'keyword'
    date_fieldName = 'date'
    text_fieldName = 'text'
    duplicateChecker_fieldNames = ['id'] # 중복 체크 기준(and), 없으면 []

    def __init__(self):
        #from db_setting
        self.db = Sql(dbName=db_setting.DB_NAME,
                      hostIP=db_setting.HOST_IP,
                      port=db_setting.PORT,
                      userID=db_setting.USER_ID,
                      password=db_setting.PASSWORD,
                      charset=db_setting.CHARSET)









