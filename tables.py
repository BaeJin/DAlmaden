from engine.dataEngine import Table_sql


##### my Item

class Table_DalmadenRegular(Table_sql) :
    tableName = 'cdata'

    fieldNames = [
        'id',
        'task_id',
        'channel',
        'keyword',
        'num',
        'post_date',
        'title',
        'text',
        'author',
        'url'
    ]

    channel_fieldName = 'channel'
    keyword_fieldName = 'keyword'
    date_fieldName = 'post_date'
    text_fieldName = 'text'
    duplicateChecker_fieldNames = ['keyword','url'] # 중복 체크 기준(and), 없으면 []


class Table_htdocsRegular(Table_sql) :
    tableName = 'htdocs'

    fieldNames = [
        'channel',
        'keyword',
        'publishtime',
        'htmltext',
        'url'
    ]

    channel_fieldName = 'channel'
    keyword_fieldName = 'keyword'
    date_fieldName = 'publishtime'
    text_fieldName = 'htmltext'
    duplicateChecker_fieldNames = ['keyword','url'] # 중복 체크 기준(and), 없으면 []












