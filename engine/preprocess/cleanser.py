import re

def cleanse_text(text) :
    text = re.sub(u"(http[^ ]*)", " ", text)
    text = re.sub(u"@(.)*\s", " ", text)
    text = re.sub(u"#", "", text)
    text = re.sub(u"[^가-힣A-z0-9?!.,]", " ", text)
    text = re.sub(u"\\s+", " ", text)

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

def cleanse_text_legacy(text) :
    text = re.sub(u"(http[^ ]*)", " ", text)
    text = re.sub(u"@(.)*\s", " ", text)
    text = re.sub(u"#", "", text)
    text = re.sub(u"[^가-힣A-z0-9?!.,]", " ", text)
    text = re.sub(u"\\s+", " ", text)
    return text.strip()


def isNewsPeoples(text, min_ratio = 0.1) :
    try :
        word_list = text.split(" ")
        list_people = ['부장', '과장','원장', '국장', '청장', '관장', '이사', '대표', '단장', '실장', '상무','전무','소장']
        count_t=len(word_list)
        count_p = 0
        for word in word_list :
            for p in list_people :
                if p in word :
                    count_p+=1
                    break
        ratio = count_p/count_t
        print(ratio)
        if  ratio >= min_ratio :
            return True
        else :
            return False
    except Exception as ex :
        print(ex)
        return False

text = '''양승태 전 대법원장 시절 핵심 고위 법관은 대법원에서 헌법재판소의 내부 정보를 파악하도록 한 것은 헌재를 견제하려던 것이 아니라 국민들의 혼란을 방지하기 위해서라며 사법행정권 남용이 아니라고 부인했다. 대법원과 헌재의 판단이 서로 엇갈릴 경우 국민들이 혼선을 겪기 위해 조율을 위해 내부 정보를 확인할 필요가 있었다는 취지다.
3일 서울중앙지법 형사합의3..'''
text = cleanse_text(text)
isNewsPeoples(text)