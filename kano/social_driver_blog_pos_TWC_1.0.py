from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
batch_bool = 57

keywordA = '식생활트렌드'
channelA = 'naverblog'
langA = 'korean'
word_classA= 'noun'
fromdateA = '2014-01-01'
todateA = '2021-01-31'
typeA = 'una'
posA= 'all'
brandA = ['풀무원','pulmuone']
ratioA = None
taggedA = 1
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,tagged=taggedA,kbf=kbfA,batch_bool=batch_bool)
# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)


keywordB = "식생활트렌드"
channelB = 'naverblog'
langB = 'korean'
word_classB = 'noun'
fromdateB = '2014-01-01'
todateB = '2021-01-31'
typeB = 'una'
posB= 'all'
brandB = ['비비고','bibigo','고메']
ratioB = None
taggedB = 1
kbfB = None
sc2 = SocialListeing(brand=brandB,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,ratio=ratioB,tagged=taggedB,kbf = kbfB,batch_bool=batch_bool)

keywordC = '식생활트렌드'
channelC = 'naverblog'
langC = 'korean'
word_classC = 'noun'
fromdateC = '2014-01-01'
todateC = '2021-01-31'
typeC = 'una'
posC= 'all'
brandC = ['오뚜기']
ratioC = None
taggedC = 1
kbfC = None
sc3 = SocialListeing(brand=brandC,keyword=keywordC,channel=channelC,lang=langC,word_class=word_classC,type='una',fromdate=fromdateC,todate=todateC,hashtag=True,loc=True,pos=posC,ratio=ratioC,tagged=taggedC,kbf = kbfC,batch_bool=batch_bool)

slViz =SlVizualize([sc1,sc2,sc3])
slViz.get_wordcloud()