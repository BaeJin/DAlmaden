from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = "제철음식 11월"
channelA = 'naverblog' #'instagram' 'naverblog' 'navershopping'
langA = 'korean'
word_classA= 'nouns' ## 형용사 adjs
fromdateA = '2019-06-01'
todateA = '2021-05-31'
posA= 'all'
brandA = None
kbfA = None


sc1 = SocialListeing(keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='no_sent',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA)


slViz =SlVizualize([sc1])
slViz.get_wordcloud()
