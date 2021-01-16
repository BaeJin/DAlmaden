from kano.engine.socialListening import SocialListeing,SlVizualize
keywordA ='화장품'
channelA ='navershopping'

##언어 형태를 지정
langA = 'korean'

##리뷰면 리뷰라고 체크
type = 'review'

##명사인지 형용사인지 체크
word_classA ='noun'

pos = 'all'
# fromdateA = '0000-00-00'
# todateA = '0000-00-00'

sc1 = SocialListeing(keyword=keywordA,channel=channelA,pos='all',type=type,lang=langA,word_class=word_classA)

slViz =SlVizualize([sc1])
slViz.get_words_pos_neg()
