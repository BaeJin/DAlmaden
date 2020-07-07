import pymysql
import pandas as pd

class Sql_loader:
    def __init__(self,sql, tablename, fieldnames):
        self.__fieldnames = fieldnames
        self.__tablename = tablename
        self.__sql = sql
        self.df = pd.DataFrame()

    def addData(self, query_where, drop_duplicate=True):
        nrows0 = self.df.shape[0]
        tempDf = self.__sql.select(self.__tablename, ",".join(self.__fieldnames), query_where, asDataFrame=True)
        self.df = self.df.append(tempDf)
        addednRows = tempDf.shape[0]
        droppednRows = 0
        if drop_duplicate:
            self.df.drop_duplicates(subset=self.__fieldnames)
            addednRows = self.df.shape[0] - nrows0
            droppednRows = tempDf.shape[0] - addednRows
        print(f'addData : added {addednRows} rows (dropped {droppednRows} rows)')

class Sql:
    def __init__(self, dbName, hostIP, port, userID, password, charset='utf8mb4'):
        self.__dbName = dbName
        self.__port = port
        self.__hostIP = hostIP
        self.__userID = userID
        self.__password = password
        self.__charset = charset
        self.__conn = None
        self.__curs = None
        self.__connect()

    def __connect(self):
        self.__conn = pymysql.connect(host=self.__hostIP, port=self.__port, user=self.__userID,
                                      password=self.__password,
                                      db=self.__dbName, charset=self.__charset)
        self.__curs = self.__conn.cursor(pymysql.cursors.DictCursor)

    def __close(self):
        self.__conn.close()


    def select(self, tablename, what="", where="", asDataFrame=False):
        select_what = "*" if len(what) < 1 else what
        sql = "select %s from %s" % (select_what, tablename)
        sql = sql + " where " + where if len(where) > 1 else sql
        self.__curs.execute(sql)
        rows = self.__curs.fetchall()
        return pd.DataFrame(rows) if asDataFrame else rows

    def count(self, tablename, where=""):
        sql = "select count(*) from %s" % (tablename)
        sql = sql + " where " + where if len(where) > 1 else sql
        self.__curs.execute(sql)
        rows = self.__curs.fetchall()
        count = int(rows[0]['count(*)'])
        return count

    def update(self, tableName, rowId, colname_id='id', **params):
        if len(params) < 1: return
        set_query = '=%s,'.join(params.keys()) + '=%s'
        query = f'update {tableName} set {set_query} where {colname_id}={rowId}'
        values = self._get_executeValues(params.values())
        self.__curs.execute(query, values)
        self.__conn.commit()

    def delete(self, tableName, rowId, colname_id='id'):
        query = f'delete from {tableName} where {colname_id}={rowId}'
        self.__curs.execute(query)
        self.__conn.commit()

    def insert(self, tablename, **params):
        # e.g. insert('datatable', date = '20150305', title = '테스트')

        sql = "insert into %s(" % (tablename) + ",".join([str(k) for k in params.keys()]) + ") values(" + \
              ",".join(["%s"] * len(params)) + ")"

        vs = self._get_executeValues(params.values())
        self.__curs.execute(sql, vs)
        row_id = self.__curs.lastrowid
        self.__conn.commit()
        return row_id

    def insert_withoutDuplication(self, tablename, check_list, **params):
        '''
        e.g. insert_withoutDuplication('datatable', ['keyword','url'],    keyword = 'abc', url = 'http://', date = '20150305', title = '테스트')
        '''
        new_params = {}
        for k, v in params.items():
            if k in check_list:
                new_params[k] = v
        if self.check_duplication(tablename, **new_params):
            print('duplicated')
            return None
        else:
            return self.insert(tablename, **params)

    def check_duplication(self, tablename, **params):
        select_where = " and ".join([k + "=" + v for k, v in params.items()])
        count = self.count(tablename, where=select_where)
        if count > 0:
            return True
        else:
            return False

    def _get_executeValues(self, inputValues):
        executeValues = [v if (type(v) is int or type(v) is float) else str(v) if v else None for v in inputValues]
        executeValues = tuple(executeValues)
        return executeValues