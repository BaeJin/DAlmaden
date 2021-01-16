from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
keywordA = '티구시포'
channelA = 'naverblog'
langA = 'korean'
word_classA= 'noun'
fromdateA = '2020-01-01'
todateA = '2020-12-31'
typeA = 'una'
posA= 'pos'
brandA = None
ratioA = None
taggerdA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,taggerd=taggerdA)

slViz =SlVizualize([sc1])
slViz.get_words_pos_neg()