from kano.engine.socialListening import SocialListeing,SlVizualize
#긍부정 아니고 키워드 비교 듀얼클라우드
keywordA ='비비고 사골곰탕'
keywordB = '착한들 사골곰탕'
channelA ='navershopping'

##언어 형태를 지정
langA = 'korean'

##리뷰면 리뷰라고 체크
type = 'navershopping_review'

##명사인지 형용사인지 체크
word_classA ='nouns'

pos = 'all'
# 네이버 쇼핑이면 POS NEG
# fromdateA = '0000-00-00'
# todateA = '0000-00-00'

sc1 = SocialListeing(keyword=keywordA,channel=channelA,pos='all',type=type,lang=langA,word_class=word_classA)
sc2 = SocialListeing(keyword=keywordB,channel=channelA,pos='all',type=type,lang=langA,word_class=word_classA)

slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()