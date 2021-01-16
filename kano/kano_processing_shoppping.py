import pymysql
import pandas as pd
import numpy as np
import os
from os.path import dirname
from sqlalchemy import create_engine
import time

##기능 추출 엑셀 파일 읽기

engine = create_engine(
    ("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8").format('datacast',
                                                           'radioga12!',
                                                           'datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                                                           3306,
                                                           'salmaden'),
    encoding='utf-8')
connect_engine = engine.connect()
conn = pymysql.connect(host='datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com',
                       user='datacast', password='radioga12!', db='salmaden', charset='utf8mb4')
curs = conn.cursor(pymysql.cursors.DictCursor)

def read_function_data():
    base = dirname(__file__)
    function_data_filename = 'process_table_shopping.xlsx'
    function_data_dir = '{}/req/'.format(base)
    function_data_path = '{}/{}'.format(function_data_dir, function_data_filename)

    function_data = pd.read_excel(function_data_path)
    return function_data

def insert_task(function_data):

    ##insert to kano_task
    already_exists_task_ids = []

    ##kano_task 에서
    sql_select_kano_task = 'select * from task'
    curs.execute(sql_select_kano_task)
    rows = curs.fetchall()
    for row in rows:
        already_exists_task_ids.append(row['id'])

    table_kano_task = function_data.loc[:, ['id', 'name', 'product_category','channel','fromdate','todate']]
    table_kano_task = table_kano_task.drop_duplicates(['id'])
    for i in table_kano_task.index:
        task_id = table_kano_task._get_value(i,'id')
        if task_id not in already_exists_task_ids:

            ##kano_task 중복 검사
            ##0. select * from kano_task
            table_kano_task_not_exist = table_kano_task[table_kano_task['id']==task_id]

            ## 1. db insert : kano_task table 에 id,name, product_category 칼럼 내용 삽입
            ## ex) 1. 강승찬 레플리카
            table_kano_task_not_exist.to_sql(name='task', con=engine, if_exists='append', index=False)


def insert_category(function_data):

    ##insert to kano_category
    already_exists_categories = []
    sql_select_kano_category = 'select * from category'
    curs.execute(sql_select_kano_category)
    rows = curs.fetchall()

    for row in rows:
        already_kano_category_dict = {row['task_id']:row['category1']}
        already_exists_categories.append(already_kano_category_dict)

###엑셀에 있는 process table 읽어오기
    table_kano_category = function_data.loc[:, ['id', 'category1']]
    table_kano_category = table_kano_category.drop_duplicates(['id', 'category1'])
    table_kano_category.rename(columns={"id":"task_id"},inplace=True)
    for i in table_kano_category.index:
        kano_task_id = table_kano_category._get_value(i,'task_id')
        category1 = table_kano_category._get_value(i,'category1')
        kano_category_dict = {kano_task_id:category1}
        if kano_category_dict not in already_exists_categories:
            table_kano_category_not_exist = table_kano_category[(table_kano_category['task_id'] == kano_task_id) & (table_kano_category['category1'] == category1)]
            table_kano_category_not_exist.to_sql(name='category', con=connect_engine, if_exists='append', index=False,schema='salmaden')

def insert_keyword(function_data):

    ##insert to kano_keyword
    already_exists_keywords = []
    sql_select_kano_keyword = 'select * from kano_keyword'
    curs.execute(sql_select_kano_keyword)
    rows = curs.fetchall()

    for row in rows:
        already_kano_keyword = row['keyword']
        already_exists_keywords.append(already_kano_keyword)

    table_kano_keyword = function_data.loc[:, ['keyword']]
    table_kano_keyword = table_kano_keyword.drop_duplicates(['keyword'])
    for i in table_kano_keyword.index:
        kano_keyword = table_kano_keyword._get_value(i, 'keyword')
        if kano_keyword not in already_exists_keywords:
            table_kano_keyword_not_exist = table_kano_keyword[table_kano_keyword['keyword'] == kano_keyword]
            table_kano_keyword_not_exist.to_sql(name='kano_keyword', con=connect_engine, if_exists='append', index=False)

def insert_cate_keyword(function_data):

    rows = pd.read_sql('select * from category', connect_engine)
    rows = rows.to_dict(orient='record')
    #insert into cate_keyword
    table_kano_cate_keyword = function_data.loc[:,['id','category1','keyword']]
    table_kano_cate_keyword = table_kano_cate_keyword.drop_duplicates(['id','category1','keyword'])

    table_kano_cate_keyword.rename(columns={'id':'task_id'},inplace=True)
    # sql_select_category_id = 'select * from category'
    # curs.execute(sql_select_category_id)
    # rows = curs.fetchall()

    for index,row in enumerate(rows):
        cate_id = row['id']     ##448
        kano_task_id = row['task_id']  ##3
        category1 = row['category1']        ##학습
        table_kano_cate_keyword_choiced = table_kano_cate_keyword[(table_kano_cate_keyword['task_id'] == kano_task_id) & (table_kano_cate_keyword['category1']==category1)]
        table_kano_cate_keyword_choiced = table_kano_cate_keyword_choiced.copy()
        table_kano_cate_keyword_choiced.loc[:,'cate_id'] = cate_id
        for i in table_kano_cate_keyword_choiced.index:
            fc_kano_cate_id = table_kano_cate_keyword_choiced._get_value(i,'cate_id')   ##448
            fc_kano_keyword = table_kano_cate_keyword_choiced._get_value(i,'keyword')   ##공부
            sql_check_cate_keyword = "select count(*) from cate_keyword where cate_id=\'%s\' and keyword=\'%s\'"%(fc_kano_cate_id,fc_kano_keyword)
            curs.execute(sql_check_cate_keyword)
            rows = curs.fetchall()
            already_cate_keyword_row_num = rows[0]['count(*)']
            print(sql_check_cate_keyword)
            print('num(rows):',already_cate_keyword_row_num)
            if already_cate_keyword_row_num ==0:
                table_kano_cate_keyword_choiced_to_db = table_kano_cate_keyword_choiced[(
                        table_kano_cate_keyword_choiced['task_id'] == kano_task_id)&(
                        table_kano_cate_keyword_choiced['cate_id'] == fc_kano_cate_id)&(
                        table_kano_cate_keyword_choiced['keyword'] == fc_kano_keyword
                        )]
                table_kano_cate_keyword_choiced_to_db = table_kano_cate_keyword_choiced_to_db.loc[:1, ['cate_id', 'keyword']]
                print(table_kano_cate_keyword_choiced_to_db)
                table_kano_cate_keyword_choiced_to_db.to_sql(name='cate_keyword', con=connect_engine, if_exists='append', index=False)
            print('********************')
        print('-------------------end-----------------')

def insert_db():
    pass

### 1. data 읽기
function_data = read_function_data()

### 2. db 연결해서 insert
##2.1 task db에 입력
insert_task(function_data)

##2.2 category db에 입력
insert_category(function_data)

##2.3 keyword db에 입력
insert_keyword(function_data)

##2.4 cate_keyword db에 입력
insert_cate_keyword(function_data)