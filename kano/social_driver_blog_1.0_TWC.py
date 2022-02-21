from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
# naverblog , instagram
keywordA = "침대 매트리스"
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns'                #형용사 adjs
fromdateA = '2012-01-01'
todateA = '2015-12-31'
posA= 'all'                         #긍정 : pos, 부정: neg, 긍부정전체: all
brandA = None                       #['brand_name1','brand_name2','brand_name3']
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

# keywordB = "TGIF' or keyword='메드포갈릭' or keyword='애슐리' or keyword='빕스"

keywordB = "침대 매트리스"
channelB = 'naverblog'
langB = 'korean'
word_classB = 'nouns'
fromdateB = '2016-01-01'
todateB = '2018-12-31'
posB = 'all' #긍정 : pos, 부정: neg, 긍부정전체: all
brandB = None
ratioB = None
kbfB = None

keywordC = '침대 매트리스'
channelC = 'naverblog'
langC = 'korean'
word_classC = 'nouns'
fromdateC = '2019-01-01'
todateC = '2021-11-30'
typeC = 'una'
posC= 'all'
brandC = None
ratioC = None
kbfC = None

sc1 = SocialListeing(keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='no_sent',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA)
sc2 = SocialListeing(keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='no_sent',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB)
sc3 = SocialListeing(keyword=keywordC,channel=channelC,lang=langC,word_class=word_classC,type='no_sent',fromdate=fromdateC,todate=todateC,hashtag=True,loc=True,pos=posC)

slViz =SlVizualize([sc1,sc2,sc3])
slViz.get_wordcloud()