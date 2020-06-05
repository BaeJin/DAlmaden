import re

def cleanse_text(text) :
    text = cleanse_text_legacy(text)
    text = text.replace(" .",".")
    text = text.replace(" ,",",")
    text = text.replace(" !","!")
    text = text.replace(" ?","?")
    text = text.replace(".",". ")
    text = text.replace(",",", ")
    text = text.replace("!","! ")
    text = text.replace("?","? ")
    text = re.sub(u"\\s+", " ", text)
    text = re.sub(u" [^가-힣A-z0-9] ", "", text)
    return text

def cleanse_text_light(text) :
    text = text.strip()
    return text

def cleanse_text_legacy(text) :
    text = re.sub(u"<.+?>"," ",text)
    text = re.sub(u"(http[^ ]*)", " ", text)
    text = re.sub(u"@(.)*\s", " ", text)
    text = re.sub(u"#", "", text)
    text = re.sub(u"[^가-힣A-z0-9?!.,]", " ", text)
    text = re.sub(u"\\s+", " ", text)
    text = text.strip()
    return text

def isBugo(text, min_ratio = 0.1) :
    keywords = ['발인','장례','별세','병원',
                '장인상','장모상','모친상','부친상','조모상','조부상']
    ratio = _getKewordsRatio_(text,keywords)
    judge = True if ratio >= min_ratio else False
    print(ratio)
    return judge

def isNewsPeoples(text, min_ratio = 0.1) :
    keywords = ['부장', '과장','원장', '국장', '청장', '관장', '이사', '대표', '단장', '실장', '상무','전무','소장']
    ratio = _getKewordsRatio_(text,keywords)
    judge = True if ratio >= min_ratio else False
    return judge

def _getKewordsRatio_(text,keywords) :
    word_list = text.split(" ")
    count_t=len(word_list)
    count_p = 0
    for word in word_list :
        for p in keywords :
            if p in word :
                count_p+=1
                break
    ratio = count_p/(count_t+1)
    return ratio
