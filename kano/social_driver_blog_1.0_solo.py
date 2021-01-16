from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
keywordA = '드라이기'
channelA = 'naverblog'
langA = 'korean'
word_classA= 'noun'
fromdateA = '2018-01-01'
todateA = '2018-12-31'

fromdateB = '2019-01-01'
todateB = '2019-12-31'

fromdateC = '2020-01-01'
todateC = '2020-12-31'

typeA = 'una'
posA= 'all'
taggedA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'


sc1 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA)
sc2 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posA)
sc3 = SocialListeing(tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateC,todate=todateC,hashtag=True,loc=True,pos=posA)

# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)

slViz =SlVizualize([sc1,sc2,sc3])
slViz.get_wordcloud()
