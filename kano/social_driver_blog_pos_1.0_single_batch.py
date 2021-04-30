from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

batch_bool = 96

keywordA = "부대찌개"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns'
fromdateA = '2019-01-01'
todateA = '2020-12-31'
typeA = 'una'
posA= 'all'
brandA = None
ratioA = None
taggedA = 1
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,tagged=taggedA,kbf=kbfA,batch_bool=batch_bool)
# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)


slViz =SlVizualize([sc1])
slViz.get_wordcloud()
