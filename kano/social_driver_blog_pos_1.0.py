from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = "식생활' or keyword='음식' or keyword='식습관' or keyword='식사' or keyword='먹거리' or keyword='아침밥' " \
           "or keyword='점심밥' or keyword='저녁밥' or keyword='요리' or keyword='식단"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'noun'
fromdateA = '2015-01-01'
todateA = '2021-01-31'
typeA = 'una'
posA= 'all'
brandA = ['풀무원','pulmuone']
ratioA = None
taggedA = None
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,tagged=taggedA,kbf=kbfA)
# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)


keywordB = "식생활' or keyword='음식' or keyword='식습관' or keyword='식사' or keyword='먹거리' or keyword='아침밥' " \
           "or keyword='점심밥' or keyword='저녁밥' or keyword='요리' or keyword='식단"
channelB = 'naverblog'
langB = 'korean'
word_classB = 'noun'
fromdateB = '2015-01-01'
todateB = '2021-01-31'
typeB = 'una'
posB= 'all'
brandB = ['비비고']
ratioB = None
taggedB = None
kbfB = None
sc2 = SocialListeing(brand=brandB,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,ratio=ratioB,tagged=taggedB,kbf = kbfB)

slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()
