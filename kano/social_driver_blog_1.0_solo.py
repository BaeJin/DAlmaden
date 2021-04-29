from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = "아웃백"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns' ## 형용사 adjs
fromdateA = '2010-05-01'
todateA = '2021-04-31'
posA= 'all'
brandA = None
kbfA = None


sc1 = SocialListeing(tagged=1,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA)


slViz =SlVizualize([sc1])
slViz.get_wordcloud()
