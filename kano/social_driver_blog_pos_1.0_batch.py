from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

batch_bool = 57

keywordA = "식생활트렌드 비비고"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'noun'
fromdateA = '2015-01-01'
todateA = '2021-01-31'
typeA = 'una'
posA= 'pos'
brandA = ['비비고','bibigo']
ratioA = None
taggedA = None
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,tagged=taggedA,kbf=kbfA,batch_bool=batch_bool)
# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)


keywordB = "식생활트렌드 비비고"
channelB = 'naverblog'
langB = 'korean'
word_classB = 'noun'
fromdateB = '2015-01-01'
todateB = '2021-01-31'
typeB = 'una'
posB= 'neg'
brandB = ['비비고','bibigo']
ratioB = None
taggedB = None
kbfB = None
sc2 = SocialListeing(brand=brandB,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,ratio=ratioB,tagged=taggedB,kbf = kbfB,batch_bool=batch_bool)


slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()