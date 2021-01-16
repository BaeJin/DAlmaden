import pandas as pd
from engine.sql.almaden import Sql
from pathlib import Path
import json

db =Sql("datacast2")
cwd = str(Path.cwd())
file = "source/unix_kbf.xlsx"
data_dict={}
df = pd.read_excel(f"{cwd}/{file}")
category_list = list(set(list(df["카테고리"])))
for i in category_list:
    keyword_df = df[df["카테고리"]==i]["키워드(소)"]
    keyword_list = list(keyword_df)
    data_dict[i] = keyword_list
data_to_json = json.dumps(data_dict,ensure_ascii=False)
print(data_to_json)
db.insert("request_analysis",
          batch_id=15,
          kbf_nouns=data_to_json)