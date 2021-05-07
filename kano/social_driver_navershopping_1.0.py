from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = "캠핑 음식"
channelA = 'navershopping'
langA = 'korean'
word_classA= 'nouns'
typeA = 'navershopping_product'
posA= 'all'
top100 = False
brandA = None
ratioA = None
kbfA = None
filter = 0
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

# keywordB = "keyword='아웃백' or keyword='TGIF' or keyword='메드포갈릭' or keyword='애슐리' or keyword='빕스"
# keywordB = "스테이크 레스토랑"
# channelB = 'naverblog'
# langB = 'korean'
# word_classB = 'nouns'
# fromdateB = '2019-01-01'
# todateB = '2021-04-31'
# typeB = 'una'
# posB = 'all'
# brandB = None
# ratioB = None
# taggedB = 1
# kbfB = None

sc1 = SocialListeing(keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type=typeA,pos=posA,filter=filter,top100=top100)



slViz =SlVizualize([sc1])
slViz.get_wordcloud()
