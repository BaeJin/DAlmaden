import json
import pandas as pd
from .settings import engine
from .utility import get_from_date, lst_to_querystr, df_read_sql, df_to_sql


class Batch :
    def __init__(self, batch_id = None, request_batch_json=None, engine=engine):
        self.task_ids = None
        self.df_task = None
        self.batch_id = batch_id
        self.batch = None
        self.df_contents = None
        self.df_sentence = None
        self.dict_batch = None
        self.engine = engine
        if request_batch_json is None and batch_id is None : raise AttributeError
        if request_batch_json :
            self.dict_batch = json.loads(request_batch_json)

        self._get_df_batch_from_db(self.dict_batch)

        if self.batch is None :
            print('creating request_batch\t')
            self._get_df_batch_from_dict(self.dict_batch)


    def _get_df_batch_from_dict(self, dict_batch):
        self.batch = pd.DataFrame.from_dict(dict_batch, orient='index').transpose()

    def _get_df_batch_from_db(self, dict_batch):
        if self.batch_id :
            query = 'select * from request_batch where batch_id = "%s"' % (self.batch_id)
        else :
            query = 'select * from request_batch where batch_name = "%s" and user_id = %s' % (
                dict_batch['batch_name'],
                dict_batch['user_id'])
        request_batch = df_read_sql(query, self.engine)
        print(request_batch)
        print(len(request_batch), 'batches found @request_batch')
        try :
            self.batch = request_batch.iloc[[(len(request_batch) - 1)]]
            print(self.batch)
            self.batch_id = self.batch.loc[0, 'batch_id']
            print('batch loaded. batch_id : ', self.batch_id)
        except Exception as ex:
            print(ex)

    def post_crawl_request(self):
        df_crawl_request_base = self.batch[['until_date', 'n_periods', 'n_crawl',
                                                'by_year','last_period_n_mult','user_id']]
        df_crawl_request = pd.DataFrame()
        for channel in self.batch.loc[0,'channels'] :
            print(channel)
            for keyword in self.batch.loc[0,'search_keywords'] :
                print(keyword)
                df_crawl_request_temp = df_crawl_request_base.copy()
                df_crawl_request_temp['batch_id'] = self.batch_id
                df_crawl_request_temp['channel'] = channel
                df_crawl_request_temp['keyword'] = keyword
                df_crawl_request = df_crawl_request.append(df_crawl_request_temp)
                print(df_crawl_request_temp)
        df_to_sql(df_crawl_request,'crawl_request',self.engine)
        print(len(df_crawl_request),'rows crawl_request posted @crawl_request')

    def post_request_batch(self):
        df_to_sql(self.batch, 'request_batch', self.engine)
        self._get_df_batch_from_db(self.dict_batch)

    def get_df_task(self):
        query = 'select task_ids, keyword, channel, crawl_status from crawl_request where batch_id = %s'%(
            self.batch_id)
        print(query)
        df_crawl_request = df_read_sql(query, engine)
        #print(df_crawl_request)

        task_ids = [task_id for task_ids in df_crawl_request['task_ids'] if task_ids is not None for task_id in task_ids]
        if len(task_ids) == 0 :
             print('no tasks detected @crawl_task')
             return
        print(len(task_ids),'tasks detected @crawl_task')
        self.task_ids = task_ids

        print(str(tuple(self.task_ids)))
        query = 'select * from crawl_task where task_id in' + str(tuple(self.task_ids))
        print(query)
        self.df_task = df_read_sql(query, engine)
        print(self.df_task)
        not_ready = self.df_task.loc[self.df_task['crawl_status'] != 'GF', :]

        print(not_ready)
        print(len(self.df_task)-len(not_ready),f"/",len(self.df_task), 'Task Executed')

        n_crawled_sum = self.df_task.groupby(['channel', 'from_date']).sum()['n_crawled']
        n_total_sum = self.df_task.groupby(['channel','from_date']).sum()['n_total']
        #print(n_total_sum)

        print(n_crawled_sum.sum(),f"/",n_total_sum.sum(), 'Contents crawled')
        #그래프 그리자

    def get_df_buzz(self) :
        query = 'select * from crawl_merged where task_id in' + str(tuple(self.task_ids))
        self.df_sentence = df_read_sql(query, engine)
        self.df_sentence['post_date1'] = [d.replace(day=1).strftime("%Y-%m-%d") if d
                                          is not None else None for d in self.df_sentence['post_date']]
        self.df_contents = self.df_sentence[
            ['task_id', 'contents_id', 'channel', 'keyword', 'post_date','post_date1','product_name','n_reply','n_like','n_reply_crawled']
        ].drop_duplicates()

    def get_df_buzz_channel(self, channelname):
        df_task = self.df_task.loc[self.df_task['channel'] == channelname]
        df_contents = self.df_contents.loc[self.df_contents['channel'] == channelname]
        df_sentence = self.df_sentence.loc[self.df_sentence['channel'] == channelname]
        return df_task, df_contents, df_sentence