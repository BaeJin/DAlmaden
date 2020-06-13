import os
class DBSetting :
    DBNAME = 'dalmaden'
    LOADING_COLUMNS = ["id","channel","keyword","post_date","text","url"]
    COLNAME_CHANNEL = 'channel'
    COLNAME_TEXT = 'text'
    COLNAME_POST_DATE = 'post_date'
    COLNAME_SENTIMENT = 'sentiment'
    COLNAME_ID = 'id'
    COLNAME_TITLE = 'title'
    COLNAME_KEYWORD = 'keyword'
    COLNAME_URL = 'url'

class FileSetting :
    FILEPATH = os.getcwd() + "\\files\\"