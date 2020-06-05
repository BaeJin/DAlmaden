import re

def cleanse(text) :
    #DB 저장을 위한 최소한의 클린징
    text = re.sub(u"[^\x20-\x7E가-힣]"," ",text)
    text = re.sub(u"\\s+", " ", text)
    return text.strip()
