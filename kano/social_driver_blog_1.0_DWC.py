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

# keywordB = "keyword='아웃백' or keyword='TGIF' or keyword='메드포갈릭' or keyword='애슐리' or keyword='빕스"
keywordB = "캠핑 음식"
channelB = 'navershopping'
langB = 'korean'
word_classB= 'nouns'
typeB = 'navershopping_product'
posB= 'all'
top100 = False
brandB = None
ratioB = None
kbfB = None

keywordC = "캠핑 음식"
channelC = 'instagram'
langC = 'korean'
word_classC= 'nouns'
fromdateC = '2018-05-01'
todateC = '2021-05-31'
typeC = 'una'
posC= 'all'
brandC = None
ratioC = None
taggedC = 1
kbfC = None

sc1 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,pos=posA,filter=filter)


sc2 = SocialListeing(keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type=typeB,pos=posB,filter=filter,top100=top100)
sc3 = SocialListeing(tagged=taggedC,keyword=keywordC,channel=channelC,lang=langC,word_class=word_classC,type='una',fromdate=fromdateC,todate=todateC,pos=posC,filter=filter)

slViz =SlVizualize([sc1,sc2,sc3])
slViz.get_wordcloud()
