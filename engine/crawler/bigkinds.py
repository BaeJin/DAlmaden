import requests
import json
import math
from crawler_utils import Sql
from crawler_utils import cleanse

URL = 'https://www.bigkinds.or.kr/api/news/search.do'
CONTENT_URL_BASE='https://www.bigkinds.or.kr/news/detailView.do?docId='
NperPage = 10000
POSTDATA = {
    "indexName": "news",
    "searchKey": "코로나",
    "searchKeys": [{}],
    "byLine": "",
    "searchFilterType": "1",
    "searchScopeType": "1",
    "searchSortType": "date",
    "sortMethod": "date",
    "mainTodayPersonYn": "",
    "startDate": "2019-12-09",
    "endDate": "2020-03-09",
    "newsIds": [],
    "categoryCodes": [],
    "providerCodes": [],
    "incidentCodes": [],
    "networkNodeType": "",
    "topicOrigin": "",
    "dateCodes": [],
    "startNo": 1, #페이지
    "resultNumber": 10,
    "isTmUsable": False,
    "isNotTmUsable": False
}
CUSTOM_HEADER = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
    'referer': '',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def crawl(keyword, startDate, endDate, nCrawl=1, comment = 'bigkinds'):
    channel = "bigkinds"
    db = Sql('cdata', comment)
    n = 0
    i = 1 #페이지 index
    retry = 0
    limit_i = 1
    task_id = None
    while n < nCrawl :
        postdata = POSTDATA.copy()
        postdata["searchKey"] = keyword
        postdata["startDate"] = startDate
        postdata["endDate"] = endDate
        postdata["startNo"] = i             #page No
        postdata["resultNumber"] = NperPage
        header= CUSTOM_HEADER
        header['referer'] = URL
        r = requests.post(URL, data=json.dumps(postdata),headers=header)
        print('engines_bigkinds_crawl_urls', keyword, i)
        print(startDate, endDate,i, 'status_code :',r.status_code)

        if r.status_code==200 :
            retry = 0
            r_json = r.text
            r_dict0 = json.loads(r_json)
            totalN = r_dict0["totalCount"]
            if nCrawl==1 : nCrawl = totalN
            if i == 1: print('기사 수 :', totalN)
            if n == 0 :
                task_id = db.insert('task_log',
                                    channel=channel,
                                    keyword=keyword,
                                    startDate=startDate,
                                    endDate=endDate,
                                    nTotal=totalN,
                                    nCrawl=nCrawl,
                                    comment=comment)
            limit_i = math.ceil(totalN/NperPage)
            r_dicts = r_dict0["resultList"]
            if len(r_dicts)>0 :
                for r_dict in r_dicts: # row by row
                    n+=1
                    try:
                        #postID = None #자동 증가
                        keyword = keyword
                        totalN = totalN
                        num = n
                        #scrapTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        url  = CONTENT_URL_BASE + r_dict["NEWS_ID"]  # r_dict["url"]
                        post_date = r_dict['DATE'][0:4] + '-' + r_dict['DATE'][4:6] + '-' + r_dict['DATE'][6:8]
                        title = r_dict["TITLE"]
                        author = r_dict["PROVIDER"] + "_" + r_dict["BYLINE"]
                        #summary = r_dict["CONTENT"]
                        provider_url = r_dict["PROVIDER_LINK_PAGE"] #probider url
                        subject = r_dict["PROVIDER_SUBJECT"] #주제
                        category1 = r_dict["CATEGORY_NAMES"] #카테고리명
                        header_content = CUSTOM_HEADER
                        header_content['referer']=url
                        r2 = requests.get(url, header=header_content).text
                        data_json = json.loads(r2)
                        r_dict2 = data_json['detail']

                        content = r_dict2["CONTENT"]
                        category2 = r_dict2["CATEGORY"]  # 카테고리
                        bk_sim = r_dict2["TMS_SIMILARITY"]  # 시소로스
                        bk_sen = r_dict2["TMS_SENTIMENT_CLASS"]  # bigkinds 감정분석 결과
                        #bk_nlp = r_dict2["TMS_NE_STREAM"]  # bigkinds 형태소 분석 결과
                        #bk_com = r_dict2["quotResult"]  # 등장하는 코멘트
                        #print(bk_com)

                        #print(bk_com)
                        #####

                        text = cleanse(content)

                        db.insert('cdata',
                                  task_id = task_id,
                                  keyword=keyword,
                                  channel=channel,
                                  num=num,
                                  post_date=post_date,
                                  title=title,
                                  text=text,
                                  author=author,
                                  url=url,
                                  url_sub=provider_url,
                                  etc1=subject,
                                  etc2=category1,
                                  etc3=category2,
                                  etc4=bk_sim,
                                  etc5=bk_sen
                        )
                        if n % 100 == 0:
                            print('\tpreprocess',n, post_date, title)
                        retry = 0


                    except Exception as ex:
                        print('aaa',ex)
                        retry += 1
                        if retry == 5:
                            print('connect loss')
                            return
                i += 1
            else :
                print('crawl ended')
                break
        else :
            retry += 1
            print('retry :' ,retry)
        if retry == 5 or i > limit_i :
            print('engines_bigkinds_crawl_urls', keyword, startDate, endDate)
            print('crawl ended', n,"/",totalN)
            break
    return