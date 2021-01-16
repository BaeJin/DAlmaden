import pandas as pd
import os
from eunjeon import Mecab
from collections import Counter
from sqlalchemy import create_engine

engine = create_engine(
    ("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8").format('root', 'robot369', '106.246.169.202', 3306, 'excel'),
    encoding='utf-8')

nlp = Mecab()


dir = os.path.dirname(os.path.realpath(__file__))
jongro = pd.read_excel(dir+"/kano/req/jongro_data.xlsx", sheet_name='설문지 주관식 응답')

print(jongro)

jongro_text = jongro.iloc[:,8:14]
print(jongro_text.columns.values)
jongro_col_list = jongro_text.columns.values

total_text_list = []
for col in jongro_col_list:
    for index in jongro_text.index:
        row_text = jongro_text._get_value(index,col)

        if not (row_text=='N' or type(row_text)==float or type(row_text)==int):
            row_text = row_text.replace('\n','')
            total_text_list.append(row_text)
print(total_text_list)
total_text_df = pd.DataFrame(total_text_list,columns=['text'])
total_text_df['num'] = '1'
total_text_df.to_sql(name='answer', con=engine, if_exists='append', index=False)

ngram_list = []
for text in total_text_list:
    ngram_list.extend(nlp.pos(text))

words = []
for ngram in ngram_list:
    print(ngram)
    if ngram[1] in ['NNP','NNG','VA','IC']:
        print(ngram)
        words.append(ngram[0])
print(words)
counter = Counter(words)
keyword = counter.most_common()
keyword = list(filter(lambda x : x[0] not in ['때','많','없','있'],keyword))
word_dict = dict(keyword)




compare_list = []
for i in keyword:
    # compare_dict = {'keyword': i[0], 'count':i[1], 'basic_differentiate': 1 if i[0] in basic_keylist else 0}       #기준년도 keylist 와 일치하는 keyword 를 찾고 식별값을 부여한다(일치: 1 불일치: 0)
    # compare_list.append(compare_dict)
    compare_dict = {'keyword': i[0], 'count': i[1]}  # 기준년도 keylist 와 일치하는 keyword 를 찾고 식별값을 부여한다(일치: 1 불일치: 0)
    compare_list.append(compare_dict)

compare_list_table = pd.DataFrame(compare_list, columns=(
    'keyword', 'count'))  # 엑셀에 저장하기 위해 keyword, count, basic_dfferntiate(식별값) 으로 칼럼을 만든다
compare_list_table.to_excel(
    dir+'/kano/buzz/' + 'jongro_5번주관식' + '_num_list' + '_' + '.xlsx',
    encoding="utf-8", index=True)  # 엑셀에 저장한다. 대상 키워드와 비교년도 를 제목으로 하는 파일 생성
