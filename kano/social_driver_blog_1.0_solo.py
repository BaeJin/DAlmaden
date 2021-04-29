from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = "아웃백"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns'
fromdateA = '2010-05-01'
todateA = '2021-04-31'
typeA = 'una'
posA= 'all'
brandA = None
ratioA = None
taggedA = 1
kbfA = None
filter = 0
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

# keywordB = "TGIF' or keyword='메드포갈릭' or keyword='애슐리' or keyword='빕스"
keywordB = "스테이크 레스토랑"
channelB = 'naverblog'
langB = 'korean'
word_classB = 'nouns'
fromdateB = '2010-05-01'
todateB = '2021-04-31'
typeB = 'una'
posB = 'all'
brandB = None
ratioB = None
taggedB = 1
kbfB = None

sc1 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,filter=filter)


sc2 = SocialListeing(tagged=taggedB, keyword=keywordB,channel=channelA,lang=langA,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,filter=filter)

slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()
