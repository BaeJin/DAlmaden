from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = "아웃백"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns'
fromdateA = '2011-01-01'
todateA = '2014-12-31'
typeA = 'una'
posA= 'all'
brandA = None
ratioA = None
taggedA = None
kbfA = None
filter = 0
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,filter=filter)


keywordB = "아웃백"
channelB = 'naverblog'
langB = 'korean'
word_classB = 'noun'
fromdateB = '2015-01-01'
todateB = '2018-12-31'
typeB = 'una'
posB= 'all'
brandB = None
ratioB = None
taggedB =None
kbfB = None
sc2 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posA,filter=filter)

keywordC = '아웃백'
channelC = 'naverblog'
langC = 'korean'
word_classC = 'noun'
fromdateC = '2019-01-01'
todateC = '2021-04-30'
typeC = 'una'
posC= 'all'
brandC = None
ratioC = None
taggedC =None
kbfC = None
sc3 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateC,todate=todateC,hashtag=True,loc=True,pos=posA,filter=filter)

slViz =SlVizualize([sc1,sc2,sc3])
slViz.get_wordcloud()
