from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()
filenameA = "캠핑전골"
keywordA = "캠핑밀푀유나베' or keyword='캠핑전골' or keyword='캠핑스키야키' or keyword='캠핑샤브샤브' or keyword='캠핑부대찌개' or keyword='캠핑곱창전골"
# keywordA = "캠핑꼬치"
channelA = 'instagram'
langA = 'korean'
word_classA= 'nouns'
fromdateA = '2015-05-01'
todateA = '2021-05-31'

typeA = 'una'
posA= 'pos'
brandA = None
ratioA = None
taggedA = 1
kbfA = None
filter = 0
# fromdateB =  '2015-01-01'
# todateB = '2020-11-19'


keywordB = "캠핑밀푀유나베' or keyword='캠핑전골' or keyword='캠핑스키야키' or keyword='캠핑샤브샤브' or keyword='캠핑부대찌개' or keyword='캠핑곱창전골"
# keywordB = "캠핑꼬치"

channelB = 'instagram'
langB = 'korean'
word_classB= 'nouns'
fromdateB = '2015-05-01'
todateB = '2021-05-31'
typeB = 'una'
posB= 'neg'
brandB = None
ratioB = None
taggedB = 1
kbfB = None

sc1 = SocialListeing(file_name=filenameA,tagged=taggedA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,pos=posA,filter=filter)
sc2 = SocialListeing(file_name=filenameA,tagged=taggedA,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,pos=posB,filter=filter)

slViz =SlVizualize([sc1,sc2])
slViz.get_wordcloud()
