import re

def cleanText(text) :
    #영문한글
    text = re.sub(u"<.+?>", " ", text) #태그제거
    text = re.sub(u"(http[^ ]*)", " ", text) #링크제거
    text = re.sub(u"@(.)*\s", " ", text) #메일주소제거
    text = re.sub(u"#", "", text) #태그제거
    text = re.sub(u"[^가-힣A-z?!.,]", " ", text)  # 숫자 넣을거면 [^가-힣A-z0-9?!.,]
    text = re.sub(u"\\s+", " ", text) #공백1개
    text = text.strip()

    # 띄어쓰기 안된 문장 제거
    text = re.sub(u"[가-힣A-z0-9]{20,}","",text)

    # 구두점 단독/중복사용 제거
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


def isNewsContents(text) :
    return not (_contentsIsBugo(text) or _contentsIsPeople(text))

def isBlogContents(text) :
    return not (_contentsIsSales(text))

def _contentsIsBugo(text) :
    return _filter_by_wordsFreq(text,
                         target_words = ['발인', '장례', '별세', '병원','장인상', '장모상', '모친상', '부친상', '조모상', '조부상'],
                         min_ratio=0.07)

def _contentsIsPeople(text) :
    return _filter_by_wordsFreq(text,
                     target_words=['부장', '과장', '원장', '국장', '청장', '관장', '이사','대표', '단장', '실장', '상무', '전무', '소장'],
                     min_ratio=0.1)

def _contentsIsSales(text) :
    return _filter_by_wordsFreq(text,
                     target_words=['원'],
                     min_ratio=0.1)

def _filter_by_wordsFreq(text, target_words=[], min_ratio=0.1) :
    ratio = _getKewordsRatio_(text, target_words)
    judge = True if ratio >= min_ratio else False
    return judge


def _getKewordsRatio_(text,keywords) :
    #키워드가 포함된 단어의 비율
    word_list = text.split(" ")
    count_t=len(word_list)
    if count_t > 0 :
        count_p = 0
        for word in word_list :
            for p in keywords :
                if p in word :
                    count_p+=1
                    break
        ratio = count_p/count_t
    else :
        ratio = 0
    return ratio

def filter_by_charFreq(text, target_character, min_ratio, preset="") :
    #특정 문자의 등장 빈도
    ratio = _getCharacterRatio_(text, target_character)
    judge = True if ratio >= min_ratio else False
    return judge

def _getCharacterRatio_(text,character) :
    count_all = len(text.replace(" ",""))
    ratio = text.count(character)/count_all if count_all>0 else 0
    return ratio

def _cut_sentence(sentence, cut=300) :
    #cut : 최대 문장길이
    sentence = sentence.lstrip()
    return sentence[:cut].rstrip() if len(sentence)>cut else sentence.rstrip()