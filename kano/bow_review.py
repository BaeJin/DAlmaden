from kano.engine import socialListening


#keyword , channel 설정하기

keywords_set = [{'keyword': '김치'}]

for set in keywords_set:
    keyword = set['keyword']
    type = 'review'
    channel = 'navershopping'
    lang = 'korean'
    pos = '부정'
    mb = socialListening.Makebow(keyword, type, channel, lang, pos)
    mb.get_bow()
