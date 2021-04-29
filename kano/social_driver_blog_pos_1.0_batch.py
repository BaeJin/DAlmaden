from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

batchA = 102

langA = 'korean'
word_classA= 'nouns'
fromdateA = '2019-01-01'
todateA = '2020-12-31'
typeA = 'una'
posA= 'all'
brandA = None
taggedA = 1
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,tagged=taggedA,kbf=kbfA,batch_bool=batchA)
# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)

batchB = 97
langB = 'korean'
word_classB = 'nouns'
fromdateB = '2019-01-01'
todateB = '2020-12-31'
typeB = 'una'
posB= 'all'
brandB = None
taggedB = 1
kbfB = None
sc2 = SocialListeing(brand=brandB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,tagged=taggedB,kbf = kbfB,batch_bool=batchB)


slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()
