from engine.dataEngine import Table_sql


##### my Item

class DalmadenRegular(Table_sql) :
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
    text_fieldName = 'text'
    postDate_fieldName = 'post_date'
    duplicateChecker_fieldNames = ['keyword','url'] # 중복 체크 기준(and), 없으면 []















