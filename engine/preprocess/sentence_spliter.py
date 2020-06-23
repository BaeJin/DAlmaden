import pandas as pd
from .cleanser import cleanse_text, cleanse_sentence
from tqdm import tqdm
import kss
from nltk import tokenize


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