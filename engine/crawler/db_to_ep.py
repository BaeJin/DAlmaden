from engine.preprocess import loader
from almaden import *


with open('keyword.csv','r') as f:
    keywords = f.read().splitlines()
    keywords = keywords[1:]
    for keyword in keywords:
        channel = 'bigkinds'
        startDate = '2015-01-01'
        endDate = '2020-04-01'
        load = loader.Data(dbName='sociallistening')

        load.addData(channel, keyword, startDate, endDate, 'bigkinds',drop_duplicate_by=['keyword','url'])
        df = load.df
        print(len(df))


        inserter = Sql(dbName='almaden',port=3406,hostIP='dev.ydns.co.kr', userID='almaden', password='Dkfakeps!@#1', charset='utf8mb4')
        task_id = inserter.insert('task_log', keyword=keyword,channel=channel ,startDate=startDate,endDate=endDate,nTotal=len(df),nCrawl=len(df))

        for index in df.index:
            post_date = df._get_value(index, 'postDate')
            text = df._get_value(index,'content' )
            text = re.sub(u"(http[^ ]*)", " ",text)
            text = re.sub(u"@(.)*\s", " ",text)
            text = re.sub(u"#", "",text)
            text = re.sub(u"\\d+", " ",text)
            text = re.sub(u"[^가-힣A-Za-z]", " ",text)
            text = re.sub(u"\\s+", " ",text)
            text = text.replace('br','')
            text = text.replace('span', '')
            text = text.replace('class', '')
            text = text.replace('quot', '')

            title = df._get_value(index, 'title')
            url = df._get_value(index, 'url')

            inserter.insert('cdata',task_id=task_id, keyword=keyword, channel=channel, post_date=post_date, text=text, title=title, url=url)

# print(task_id)



# loader._load_('bigkinds', '은평 주민청원제', '2015-01-01', '2020-04-01', 'bigkinds')