from almaden import Nlp
from almaden import Sql


nlp = Nlp("hannanum")
db = Sql("sociallistening")

raw_data = db.select("navershopping",["rating","text"])

len(raw_data)
neg_text = []
pos_text = []
for d in raw_data :
    if d["rating"] < 3 :
        neg_text.append(d["text"])
    elif d["rating"] >3 :
        pos_text.append(d["text"])
n=0
for d in raw_data :
    if d["text"].find("블레이드")>0 :
        print(d["text"])
        n+=1

n
len(neg_text)

pos_bow = nlp.get_nounCount_by_list(pos_text)
neg_bow = nlp.get_nounCount_by_list(neg_text)


keywords = set(list(pos_bow.keys())+list(neg_bow.keys()))
with open("navershopping.csv","w") as f :
    for k in keywords :
        nPos = 0
        nNeg = 0
        try :
            nPos = pos_bow[k]
        except :
            pass
        try :
            nNeg = neg_bow[k]
        except :
            pass
        f.write("%s,%d,%d\n"%(k,nPos,nNeg))