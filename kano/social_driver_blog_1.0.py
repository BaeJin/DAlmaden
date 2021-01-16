from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
keywordA = '드라이기'
channelA = 'naverblog'
langA = 'korean'
word_classA= 'noun'
fromdateA = '2020-01-01'
todateA = '2020-12-31'
typeA = 'una'
posA= 'all'
brandA = ['다이슨','dyson']
ratioA = 0.47
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,taggerd=None)
# sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)


keywordB = '드라이기'
channelB = 'naverblog'
langB = 'korean'
word_classB = 'noun'
fromdateB = '2020-01-01'
todateB = '2020-12-31'
typeB = 'una'
posB= 'all'
brandB = ['jmw']
ratioB = 0.24
sc2 = SocialListeing(brand=brandB,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,ratio=ratioB, taggerd=None)

keywordC = '드라이기'
channelC = 'naverblog'
langC = 'korean'
word_classC = 'noun'
fromdateC = '2020-01-01'
todateC = '2020-12-31'
typeC = 'una'
posC= 'all'
brandC = ['유닉스','unix']
ratioC = 0.17
sc3 = SocialListeing(brand=brandC,keyword=keywordC,channel=channelC,lang=langC,word_class=word_classC,type='una',fromdate=fromdateC,todate=todateC,hashtag=True,loc=True,pos=posC,ratio=ratioC, taggerd=None)



keywordD = '드라이기'
channelD = 'naverblog'
langD = 'korean'
word_classD = 'noun'
fromdateD = '2020-01-01'
todateD = '2020-12-31'
typeD = 'una'
posD= 'all'
brandD = ['필립스','philips']
ratioD = 0.09
sc4 = SocialListeing(brand=brandD,keyword=keywordD,channel=channelD,lang=langD,word_class=word_classD,type='una',fromdate=fromdateD,todate=todateD,hashtag=True,loc=True,pos=posD,ratio=ratioD, taggerd=None)



keywordE = '드라이기'
channelE = 'naverblog'
langE = 'korean'
word_classE = 'noun'
fromdateE = '2020-01-01'
todateE = '2020-12-31'
typeE = 'una'
posE = 'all'
brandE = ['테팔','tefal']
ratioE = 0.03
sc5 = SocialListeing(brand=brandE,keyword=keywordE,channel=channelE,lang=langE,word_class=word_classE,type='una',fromdate=fromdateE,todate=todateE,hashtag=True,loc=True,pos=posE,ratio=ratioE, taggerd=None)

slViz =SlVizualize([sc1,sc2,sc3,sc4,sc5])
slViz.get_awarness_pie()