import pandas as pd
from .cleanser import cleanse_text, cleanse_sentence
from tqdm import tqdm
from kss import split_sentences
#from nltk import tokenize


def splitSentences(df, colname_text='text', newColname_sentence='sentence_text'):
    '''
    :param colnames: 행이름 str
    :param by_sentence_textColname: 문장 분해 대상 text 행이름
    :return: DataFrame
    '''
    df_new = pd.DataFrame()
    nrows = df.shape[0]
    for i in tqdm(range(nrows), "loader : Getting Sentences "):
        row = df.iloc[i]
        text = row[colname_text]
        if len(text) > 0:
            sentences = split_sentences(text)  # 텍스트 길이 300 넘는게 허다하게 나옴... 체크 필요함
            #sentences = tokenize.sent_tokenize(text)
            for s in sentences:
                s = s.strip()
                if len(s) > 0:
                    row_temp = row.copy()
                    row_temp[newColname_sentence] = s
                    df_new = df_new.append(row_temp)
        else:
            continue
    print(f"loader : Getting DataFrame Done {nrows} texts to {df_new.shape[0]} Sentences")
    return df_new




