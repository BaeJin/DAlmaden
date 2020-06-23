from almaden import Sql
from engine.preprocess.sentence_spliter import get_sentence_df
import nltk
import tqdm
import pandas as pd
nltk.download()
from collections import Counter

import pandas as pd
from engine.preprocess.cleanser import cleanse_text, cleanse_sentence
from tqdm import tqdm
import kss
from nltk import tokenize

db = Sql('salmaden')

def get_sentence_df(df, text_fieldName='text', sentence_text_fieldName='sentence_text', language = 'korean'):
    '''

    :param colnames: 행이름 str
    :param by_sentence_textColname: 문장 분해 대상 text 행이름
    :return: DataFrame
    '''

    df_new = pd.DataFrame()
    nrows = df.shape[0]
    for i in tqdm(range(nrows), "loader : Getting Sentences "):
        row = df.iloc[i]
        text = row[text_fieldName]
        if len(text) > 0:
            text = cleanse_text(text)
            if language == 'korean' :
                sentences = kss.split_sentences(text)  # 텍스트 길이 300 넘는게 허다하게 나옴... 체크 필요함
            elif language == 'english' :
                sentences = tokenize.sent_tokenize(text)
            else :
                print('no language')
                return
            for s in sentences:
                s = cleanse_sentence(s)
                if len(s) > 0:
                    row_temp = row.copy()
                    row_temp[sentence_text_fieldName] = s
                    df_new = df_new.append(row_temp)
        else:
            continue
    print(f"loader : Getting DataFrame Done {nrows} Documents to {df_new.shape[0]} Sentences")
    return(df_new)


df_product = db.select('product','id, channel, category, productName, price, url','category="hair dryer"',asDataFrame=True)
df_product = df_product.rename(columns = {'id':'product_id'})
df_product = df_product.drop_duplicates(subset=['url'])

df_dyson = db.select('review', 'product_id, rating, text','product_id = 1432',asDataFrame=True)
df_elchim = db.select('review', 'product_id, rating, text','product_id = 1470',asDataFrame=True)
df_chi = db.select('review', 'product_id, rating, text','product_id = 1602',asDataFrame=True)

df_all = pd.DataFrame()
df_all = df_all.append(df_dyson).append(df_elchim).append(df_elchim)
df_all = pd.merge(df_all, df_product, how='left', on='product_id')



df_all = get_sentence_df(df_all,language='english')

def get_nouns(text) :
    nouns = []  # empty to array to hold all nouns
    for word, pos in nltk.pos_tag(nltk.word_tokenize(str(text))):
        if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
            nouns.append(word)
    return nouns

nouns_list = []
for sent_text in tqdm(df_all['sentence_text'], 'get nouns') :
    nouns_list.append(get_nouns(sent_text))
df_all['nouns'] = nouns_list


nouns_all = []
for n in df_all['nouns'] :
    nouns_all.extend(n)
bow_dict = dict(Counter(nouns_all).most_common())
bow_df = pd.DataFrame({'keyword' : list(bow_dict.keys()), 'count' : list(bow_dict.values())})

bow_df

bow_df.to_csv("amazon_dryer_bow.csv")