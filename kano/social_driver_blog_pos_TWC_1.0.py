from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = "캠핑 음식"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns'
fromdateA = '2018-05-01'
todateA = '2021-05-31'
typeA = 'una'
posA= 'all'
brandA = None
ratioA = None
taggedA = 1
kbfA = None
filter = 0
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,pos=posA,filter=filter)


keywordB = "캠핑 음식"
channelB = 'instagram'
langB = 'korean'
word_classB = 'noun'
fromdateB = '2018-05-01'
todateB = '2021-05-31'
typeB = 'una'
posB= 'all'
brandB = None
ratioB = None
taggedB =1
kbfB = None
sc2 = SocialListeing(tagged=taggedB,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,pos=posB,filter=filter)

keywordC = "캠핑 음식"
channelC = 'navershopping'
langC = 'korean'
word_classC= 'nouns'
typeC = 'navershopping_product'
posC= 'all'
top100 = False
brandC = None
ratioC = None
kbfC = None

sc3 = SocialListeing(keyword=keywordC,channel=channelC,lang=langC,word_class=word_classC,type=typeC,pos=posC,filter=filter,top100=top100)

slViz =SlVizualize([sc1,sc2,sc3])
slViz.get_wordcloud()
