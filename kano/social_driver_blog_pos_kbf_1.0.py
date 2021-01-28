from engine.sql.almaden import Sql
from kano.engine.socialListening import SocialListeing,SlVizualize
# with open("req/big_crawling.txt", "r",encoding='utf-8') as file:
#     keyword_list= file.readlines()
#     for keywordA in keyword_list:
#         keywordA = keywordA.splitlines()

db = Sql('datacast2')
rows = db.select('''
request_batch as rb 
join crawl_request AS cr on rb.batch_id=cr.batch_id 
join crawl_request_task AS crt on crt.request_id=cr.request_id
join crawl_task AS ct on crt.task_id=ct.task_id
''', 'rb.batch_id, cr.request_id,ct.task_id,rb.batch_name,cr.keyword,sum(ct.n_crawled)',
                 'rb.batch_name LIKE \'%s\' and rb.batch_id=27 AND ct.channel !="navershopping" GROUP BY keyword ORDER BY rb.batch_id'%("%실창%"))
for row in rows:
    keywordA = row['keyword']
    channelA = 'naverblog'
    langA = 'korean'
    word_classA= 'noun'
    fromdateA = '2015-01-01'
    todateA = '2021-01-20'
    typeA = 'una'
    posA= 'pos'
    brandA = None
    ratioA = None
    taggedA = 1
    kbfA = None
    filename = row['batch_name']
    # fromdateB =  '2015-01-01'
    # todateB = '2020-11-19'

    sc1 = SocialListeing(brand=brandA,keyword=keywordA,channel=channelA,lang=langA,word_class=word_classA,type='una',fromdate=fromdateA,todate=todateA,hashtag=True,loc=True,pos=posA,ratio=ratioA,tagged=taggedA,kbf=kbfA,file_name=filename)
    # sc2 = SocialListeing(keyword=keywordB,channel=channelA,lang=langA,word_class=word_classA,type='groupby',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True)

    keywordB = row['keyword']
    channelB = 'naverblog'
    langB = 'korean'
    word_classB = 'noun'
    fromdateB = '2015-01-01'
    todateB = '2021-01-20'
    typeB = 'una'
    posB= 'neg'
    brandB = None
    ratioB = None
    taggedB = 1
    kbfB = None

    sc2 = SocialListeing(brand=brandB,keyword=keywordB,channel=channelB,lang=langB,word_class=word_classB,type='una',fromdate=fromdateB,todate=todateB,hashtag=True,loc=True,pos=posB,ratio=ratioB,tagged=taggedB,kbf=kbfB,file_name=filename)
    slViz =SlVizualize([sc1,sc2])
    slViz.get_wordcloud()
