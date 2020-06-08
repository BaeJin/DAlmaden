import re
from collections import Counter

def df_mutate_token_counter(df, tokenColumnName, duplicate_count=False) :
    rdf = df.copy()
    rdf = rdf.assign(tokens_counter=lambda dataframe: dataframe[tokenColumnName].map(Counter))
    return rdf

def get_token_counter(seqOfTokensSeq, duplicate_count=False) :
    '''
    :param seqOfTokensSeq: e.g. [['a','b','b'],['a','b','b,'c']]
    :return: {a:2, b:4, c:1}
    '''
    if duplicate_count :
        seq = [token for tokens in seqOfTokensSeq for token in tokens]
    else :
        seq = [token for tokens in seqOfTokensSeq for token in set(tokens)]
    return Counter(seq).most_common()
