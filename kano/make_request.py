import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def last_day_of_month(any_day): #datetime.datetime
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

def get_df_request_crawl(channel, keyword, until_date, n_periods, n_crawl,
                         by_year=True, use_end_date=False, last_period_n_mult=3) : #n_periods가 연단위/월단위, 마지막일 종료 여부, 마지막 기간 n_crawl

    until_date = datetime.datetime.strptime(until_date, '%Y-%m-%d').date()
    until_date = last_day_of_month(until_date) if use_end_date else until_date

    if by_year:
        n_month = n_periods * 12
        last_period_start_date = until_date - relativedelta(years=1) + relativedelta(days=1)
    else:
        n_month = n_periods
        last_period_start_date = until_date - relativedelta(months=1) + relativedelta(days=1)

    start_date = until_date - relativedelta(months=n_month) + relativedelta(days=1)
    date_ranges = []
    for i in range(n_month) :
        n_crw = n_crawl*last_period_n_mult if start_date >= last_period_start_date else n_crawl
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        date_ranges.append((start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'),n_crw))
        start_date += relativedelta(months=1)
    df_request_crawl=pd.DataFrame(date_ranges,columns=['from_date','to_date','n_crawl'])
    df_request_crawl['channel'] = channel
    df_request_crawl['keyword'] = keyword
    return df_request_crawl




sample = get_df_request_crawl('naverblog','스타벅스','2019-11-06',60,100,by_year=False,use_end_date=False)