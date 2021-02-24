import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import json
from engine.sql.almaden import Sql
from engine.crawler.crawlLibnaverblog import CrawlLibnaverBlog
from engine.crawler.crawlLibnavernews import CrawlLibnaverNews
from engine.crawler.crawlLibInstagram import CrawlLibInstagram
from engine.crawler.crawlLibnavershopping import CrawlLibNavershopping
from engine.crawler.crawlLibyoutube import CrawlLibYoutube

from engine.crawler.crawlLibAmazon import CrawlLibAmazon

import re


class RequestTask:
    def __init__(self):
        self.period_differ_channel = ['naverblog','twitter','navernews']
        self.review_channel = ['navershopping','coupang','youtube']

    def get_df_request_crawl(self,channel, keyword, until_date, n_periods, n_crawl,
                             by_year=True, use_end_date=False,
                             last_period_n_mult=1):  # n_periods가 연단위/월단위, 마지막일 종료 여부, 마지막 기간 n_crawl

        # until_date = datetime.datetime.strptime(until_date, '%Y-%m-%d').date()
        until_date = self.last_day_of_month(until_date) if use_end_date else until_date

        if by_year:
            n_month = n_periods * 12
            last_period_start_date = until_date - relativedelta(years=1) + relativedelta(days=1)
        else:
            n_month = n_periods
            last_period_start_date = until_date - relativedelta(months=1) + relativedelta(days=1)

        start_date = until_date - relativedelta(months=n_month) + relativedelta(days=1)
        date_ranges = []
        for i in range(n_month):
            n_crw = n_crawl * last_period_n_mult if start_date >= last_period_start_date else n_crawl
            end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
            date_ranges.append((start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), n_crw))
            start_date += relativedelta(months=1)
        df_request_crawl = pd.DataFrame(date_ranges, columns=['from_date', 'to_date', 'n_crawl'])
        df_request_crawl['channel'] = channel
        df_request_crawl['keyword'] = keyword
        return df_request_crawl

    def last_day_of_month(self,any_day):  # datetime.datetime

        # get close to the end of the month for any day, and add 4 days 'over'
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
        # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
        return next_month - datetime.timedelta(days=next_month.day)

    def make_task_table(self,channel,search_keyword,until_date,n_periods):
        df_request_crawl = pd.DataFrame(columns=['from_date','to_date','keyword','channel'])
        if channel in self.period_differ_channel:
            df_request_crawl = self.get_df_request_crawl(channel, search_keyword, until_date, n_periods, 100, use_end_date=True)

        ###네이버쇼핑, 쿠팡
        # elif channel in self.review_channel:
        #     tasks_df = self.get_df_request_crawl(channel, search_keyword, until_date, n_periods, 100, use_end_date=True)
        #     nvs_obj = CrawlLibNavershopping(keyword=search_keyword,n_crawl=n_crawl)
        #     df_request_crawl = nvs_obj.get_product_info_list_to_crawl()
        #     df_request_crawl['channel'] = channel
        #     df_request_crawl['from_date'] = tasks_df.iloc[0]['from_date']
        #     df_request_crawl['to_date'] = tasks_df.iloc[-1]['to_date']

        else:
            tasks_df = self.get_df_request_crawl(channel, search_keyword, until_date, n_periods, 100, use_end_date=True)
            df_request_crawl.at[0,'keyword'] = tasks_df.iloc[0]['keyword']
            df_request_crawl.at[0,'channel'] = tasks_df.iloc[0]['channel']
            df_request_crawl.at[0,'from_date'] = tasks_df.iloc[0]['from_date']
            df_request_crawl.at[0,'to_date'] = tasks_df.iloc[-1]['to_date']
            df_request_crawl.at[0,'n_crawl'] = 999999

        return df_request_crawl

    def request_to_task(self):

        ##datacast2 테이블을 선택함
        db = Sql("datacast2")

        sql_alchemy_engine = db.sql_alchemy_engine

        ##request 를 선택한다.
        request_rows = pd.read_sql("select * from crawl_request where task_ids is null and crawl_status='GR'",con=sql_alchemy_engine.connect())

        for idx in request_rows.index:
            already_task_count = 0
            task_ids = []

            ##request 한개를 가져온다.
            ##request 에서 task 를 만들기위해 칼럼 정보 가져오기 request_id, channel, keyword, until_date, n_periods
            request_id = int(request_rows.at[idx,'request_id'])
            channel = request_rows.at[idx,'channel']
            search_keyword = request_rows.at[idx, 'keyword']
            until_date = request_rows.at[idx,'until_date']
            n_periods = request_rows.at[idx,'n_periods']
            is_channel = request_rows.at[idx, 'is_channel']

            ##task 테이블을 생성한다. 네이버블로그, 네이버뉴스, 트위터는 월별로 테스크를 나눠야함. instagram , youtube 는 기간 검색이 불가능함
            ## 기간 검색이 불가능한 채널에 요청한 전체 기간에 대한 task 한개만 생성한다.
            tasks_df = self.make_task_table(channel,search_keyword,until_date,n_periods)
            tasks_df['is_channel']= is_channel
            ##생성된 task 테이블 들을 DB 에 넣어주기
            for idx in tasks_df.index:
                channel = tasks_df.at[idx, 'channel']
                is_channel = tasks_df.at[idx,'is_channel']
                keyword = tasks_df.at[idx, 'keyword']
                from_date = tasks_df.at[idx, 'from_date']
                to_date = tasks_df.at[idx, 'to_date']
                n_crawl = int(tasks_df.at[idx, 'n_crawl'])
                ##task 는 keyword, channel, from_date, to_date 기준 중복을 허용하지 않는다
                ##request 는 여러개의 task_id 를 가지고 task 또한 여러개의 requset 에 속할 수 있음 N:N 관계
                task_id = db.insert_withoutDuplication('crawl_task', ['keyword','channel','from_date','to_date','is_channel'],
                                    channel=channel,
                                    keyword=keyword,
                                    from_date=from_date,
                                    to_date=to_date,
                                    n_crawl=n_crawl,
                                    is_channel=0 if is_channel is None or is_channel==0 else 1)

                ##중복된 task_id 가 존재하지 않는 경우에는(중복x) 직전에 삽입하고 돌려받은 task_id 를 가져와서 request 와 mapping 한다.
                if task_id is not None:
                    print('중복X')
                    db.insert_withoutDuplication('crawl_request_task',['request_id','task_id'],request_id=request_id,task_id=task_id)

                    self.crawl_total_contents_num(task_id,keyword,channel,from_date,to_date,is_channel)
                ##만약 keyword,channel,from_date,to_date 기준 중복된 task 가 존재하는 경우에는 이미 존재하는 task 를 가져와서 mapping 한다.
                elif task_id is None:
                    print('중복O')
                    ##이미 존재하는 task_id 가 있을 때마다 1개 카운트 총 몇개의 task 가 중복되었는지 파악하기 위함
                    already_task_count +=1
                    ###1. 이미 존재하는 task 를 가져온다.
                    exist_select_task_sql="select task_id from crawl_task where keyword=\'%s\' and channel=\'%s\' and from_date=\'%s\' and to_date=\'%s\'"\
                        %(keyword,channel,from_date,to_date)
                    task_rows = pd.read_sql(exist_select_task_sql,con=sql_alchemy_engine.connect())
                    task_id = task_rows.get('task_id')[0]

                    self.crawl_total_contents_num(task_id,keyword,channel,from_date,to_date,is_channel)

                    ###2. task_id를 request_id 와 맵핑하고 request_task 테이블에 넣어준다.
                    db.insert_withoutDuplication('crawl_request_task',['request_id','task_id'],request_id=request_id,task_id=int(task_id))

                #task 한개 끝
                #모든 task ID
                task_ids.append(int(task_id))
            #request 한개 끝
            db.update_one('crawl_request','task_ids',json.dumps(task_ids),'request_id',request_id)
        #함수 끝
        db.close()

    def crawl_total_contents_num(self,task_id,keyword,channel,from_date,to_date,is_channel=0):
        if channel=='naverblog':
            obj = CrawlLibnaverBlog(task_id=task_id,keyword=keyword,from_date=from_date,to_date=to_date)
            obj.crawl_total()
            del obj
        if channel=='navernews':
            obj = CrawlLibnaverNews(task_id=task_id,keyword=keyword,from_date=from_date,to_date=to_date)
            obj.crawl_total()
            del obj
        if channel=='instagram':
            obj = CrawlLibInstagram(task_id=task_id,keyword=keyword)
            obj.crawl_total()
            del obj
        if channel=='navershopping':
            obj = CrawlLibNavershopping(task_id = task_id, keyword = keyword)
            obj.crawl_total()
            del obj

        if channel=='youtube':
            obj = CrawlLibYoutube(task_id=task_id, keyword=keyword, is_channel=is_channel)
            obj.crawl_total()
            del obj
        if channel=='amazon':
            obj = CrawlLibAmazon(task_id=task_id,keyword=keyword)
            obj.crawl_total()
            del obj
            pass

