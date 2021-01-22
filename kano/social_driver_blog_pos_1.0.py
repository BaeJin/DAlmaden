from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
keywordA = 'home battery'
channelA = 'youtube\' or ct.channel=\'twitter'
langA = 'english'
word_classA= 'noun'
fromdateA = '2020-01-01'
todateA = '2021-01-31'
typeA = 'una'
posA= 'pos'
brandA = None
ratioA = None
taggedA = 1
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,tagged=taggedA,kbf=kbfA)
# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)


keywordB = 'home battery'
channelB = 'youtube\' or ct.channel=\'twitter'
langB = 'english'
word_classB = 'noun'
fromdateB = '2020-01-01'
todateB = '2021-01-31'
typeB = 'una'
posB= 'neg'
brandB = None
ratioB = None
taggedB = 1
kbfB = None
sc2 = SocialListeing(brand=brandB,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,ratio=ratioB,tagged=taggedB,kbf = kbfB)

slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()
