from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
# naverblog , instagram
keywordA = "캠핑"
channelA = 'instagram'
langA = 'korean'
word_classA= 'nouns'                #형용사 adjs
fromdateA = '2018-06-01'
todateA = '2021-05-31'
posA= 'all'                         #긍정 : pos, 부정: neg, 긍부정전체: all
brandA = None                       #['brand_name1','brand_name2','brand_name3']
kbfA = None
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'

# keywordB = "TGIF' or keyword='메드포갈릭' or keyword='애슐리' or keyword='빕스"

keywordB = "김치"
channelB = 'instagram'
langB = 'korean'
word_classB = 'nouns'
fromdateB = '2018-06-01'
todateB = '2021-05-31'
posB = 'all' #긍정 : pos, 부정: neg, 긍부정전체: all
brandB = None
ratioB = None
kbfB = None

sc1 = SocialListeing(keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='no_sent',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA)


sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classB,type='no_sent',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB)

slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()
