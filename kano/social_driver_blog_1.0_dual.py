from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

keywordA = '현미밥'
channelA = 'naverblog'
langA = 'korean'
word_classA= 'nouns'                #형용사 adjs
fromdateA = '2019-05-01'
todateA = '2020-04-31'
posA= 'all'                         #긍정 : pos, 부정: neg, 긍부정전체: all
brandA = None                       #['brand_name1','brand_name2','brand_name3']
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

# keywordB = "TGIF' or keyword='메드포갈릭' or keyword='애슐리' or keyword='빕스"

keywordB = "스테이크 레스토랑"
channelB = 'naverblog'
langB = 'korean'
word_classB = 'nouns'
fromdateB = '2020-05-01'
todateB = '2021-04-31'
posB = 'all' #긍정 : pos, 부정: neg, 긍부정전체: all
brandB = None
ratioB = None
taggedB = 1
kbfB = None

sc1 = SocialListeing(tagged=1,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA)


sc2 = SocialListeing(tagged=1, keyword=keywordB,channel=channelA,lang=langA,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB)

slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()
