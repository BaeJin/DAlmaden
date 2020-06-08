import pandas as pd
import os

from engine.preprocess.loader import Data
from engine.analysis.bagOfWords import get_token_counter
from engine.analysis.tokenizer import get_nouns_list


def load_df(channel, keyword, fromDate, toDate,
            colNames = ["channel","keyword","post_date","text","url"], by_sentence = "text",
            dbName='dalmaden', tablename='cdata') :
    data = Data(dbName)
    data.addData(channel, keyword, fromDate, toDate,
                tablename=tablename, unique = True, drop_by=['keyword','url'])
    df = data.get_df(*colNames,by_sentence=by_sentence)
    return df

def get_df_bow(text_seq, type = 'noun', duplicate_count = False) :
    if type == 'noun' :
        df = get_nouns_list(text_seq)
    else :
        pass #TBD

    bow = get_token_counter(df, duplicate_count)
    df_bow = pd.DataFrame(bow)
    return df_bow

def write_csv(df, filename) :
    path = os.getcwd()+"\\files\\"+filename
    df.to_csv(path)
