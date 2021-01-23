from engine.sql.almaden import Sql
import pandas as pd
db = Sql('datacast2')

df = db.select('crawl_contents','*','task_id=25003',asDataFrame=True)
dup = df[df.duplicated(['url'])]
