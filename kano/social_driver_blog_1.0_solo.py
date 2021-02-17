from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
keywordA = "증권사 선택' or keyword='증권사 추천' or keyword='증권사 평판"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns'
fromdateA = '2013-01-01'
todateA = '2021-01-31'
typeA = 'una'
posA= 'all'
brandA = None
ratioA = None
taggedA = 1
kbfA = None
filter = 1
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'


sc1 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,filter=filter)

# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)

slViz =SlVizualize([sc1])
slViz.get_wordcloud()
