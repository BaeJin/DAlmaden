from engine.preprocess.loader import Data
from engine.analysis.bagOfWords import df_mutate_token_counter
from engine.analysis.tokenizer import df_mutate_tokens_nouns

def load_df(channel, keyword, fromDate, toDate,
            colNames = ["channel","keyword","post_date","text","url"], by_sentence = "text",
            dbName='dalmaden', tablename='cdata') :
    data = Data(dbName)
    data.addData(channel, keyword, fromDate, toDate,
                tablename=tablename, unique = True, drop_by=['keyword','url'])
    df = data.get_df(*colNames,by_sentence=by_sentence)
    return df

def get_bow(df, textColumn = 'text', type = 'noun', duplicate_count = False) :
    if type == 'noun' :
        df = df_mutate_tokens_nouns(df, textColumn)
    else :
        pass #TBD

    if duplicate_count :
        bow = df_mutate_token_counter(df, 'tokens')


def df_mutate_tokens(df, textColumn = 'text'):
    return