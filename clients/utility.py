import json
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

def save_sql(table_name, engine, single_row = False, update=False,**items) :
    if update :
        pass
    else :
        dict_data = {}
        for k,v in items.items() :
            dict_data[k] = [v] if single_row else v
        df_data = pd.DataFrame(dict_data)
        df_data.to_sql(table_name, engine, if_exists='append',index=False)


def last_day_of_month(any_day): #datetime.datetime
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

def get_from_date(until_date, n_periods, by_year=True,use_end_date = True) :

    until_date = datetime.datetime.strptime(until_date, '%Y-%m-%d').date() if type(until_date) is str else until_date
    until_date = last_day_of_month(until_date) if use_end_date else until_date

    if by_year:
        from_date = until_date - relativedelta(years=n_periods) + relativedelta(days=1)
    else:
        from_date = until_date - relativedelta(months=n_periods) + relativedelta(days=1)
    from_date = from_date.strftime('%Y-%m-%d')
    return from_date

def lst_to_querystr(list_str) :
    return "("+",".join(['"'+s+'"' for s in list_str])+")"

def keywords_in_target(search_keywords, target) :
    for sk in search_keywords :
        if sk in target :
            return True
    return False


def decode_json_df(df) :
    for column in df.columns :
        count_check = 0
        for checker in df[column] :
            if checker is not None :
                if type(checker) is str :
                    if ('{' in checker and '}' in checker) or ('[' in checker and ']' in checker) :
                        count_check += 1
                        if count_check > len(df[column])*0.1 :
                            df[column] = [(json.loads(x) if x is not None else None) for x in df[column]]
                            break
                    else :
                        break
                else :
                    break
    return df

def df_read_sql(query, engine) :
    df = pd.read_sql(query, engine)
    if df is None :
        return None
    else :
        return decode_json_df(df)

def incode_json_df(df) :
    for column in df.columns :
        for checker in df[column] :
            if checker is not None :
                if type(checker) is list or type(checker) is dict:
                    df[column] = [json.dumps(x,ensure_ascii=False) for x in df[column]]
                    break
                else :
                    break
    print(df)
    return df

def df_to_sql(df, table, engine) :
    df = incode_json_df(df)
    print(df)
    df.to_sql(table, engine, if_exists='append', index=False)

def mult_columns(vector, matrix) :
    mat_mult = np.array([vector,] * matrix.shape[1]).transpose()
    return matrix * mat_mult