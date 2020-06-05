from almaden import Sql
import pandas as pd

db = Sql("dalmaden")


p = db.select("cdata","*","keyword='복숭아'",asDataFrame = True)
p1 = p.drop_duplicates(subset=["channel","keyword","url1"])

def loadPandas(keyword, channel,