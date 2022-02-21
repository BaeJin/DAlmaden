##mongoDB cafeloader
from pymongo import MongoClient
from time import sleep
from datetime import datetime as dt
import datetime
import requests
import json
from bs4 import BeautifulSoup
import re
from engine.sql.almaden import cleanse

def get_keyhex(keyword):
    keyint = keyword.encode("UTF-8")
    keyhex = ""
    for i in keyint:
        keyhex = keyhex + '%{:02X}'.format(i)
    return keyhex


status_done = 'GF'
status_doing = 'GI'
status_do = 'GR'
status_error = 'ER'

now = datetime.datetime.now()
CUSTOM_HEADER = {'accept': 'application/json, text/plain, */*',
                            'accept-encoding': 'gzip, deflate, br',
                            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                            'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
                            'referer': 'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword=',#+heyhex
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

my_client = MongoClient("mongodb://localhost:27017/")
print(my_client.list_database_names())

mydb = my_client['cafeloader']
crawl_task = mydb['crawl_task']
crawl_contents = mydb['crawl_contents']

keyword = '에어팟 프로'
keyhex = get_keyhex(keyword)
channel = 'naverblog'
crawl_status = status_do
from_date = '2020-01-01'
to_date = '2021-03-01'
n_total = 1000
n_crawl = 100
n_crawled = 0
task_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
x = crawl_task.insert_one(
    {"channel":"naverblog",
     "keyword":29,
     "crawl_status":crawl_status,
     "from_date":from_date,
     "to_date":to_date,
     "n_total":n_total,
     "n_crawl":n_crawl,
     "n_crawled":n_crawled,
     "task_datetime":task_datetime}
)
task_id = x.inserted_id
print(task_id)

def crawl_total():

    keyhex = get_keyhex(keyword)
    custom_header = CUSTOM_HEADER
    custom_header['referer'] += keyhex
    pageNo = 1
    list_url = "https://section.blog.naver.com/ajax/SearchList.nhn?countPerPage=7&currentPage=%d&endDate=%s" % (
        pageNo, to_date) + "&keyword=%s&orderBy=sim&startDate=%s&type=post" % (keyhex, from_date)

    req = requests.get(list_url, headers=custom_header)  # custom_header를 사용하지 않으면 접근 불가
    if req.status_code == requests.codes.ok:
        r = req.text[6:]
        data_all = json.loads(r)

        ### task_log 입력
        nTotal = data_all['result']['totalCount']
        print(nTotal, 'items found for ' + keyword,task_id)
        crawl_task.update_one({'_id':task_id},{"$set":{'n_total':nTotal}})

def get_realUrl(idStr, noStr):
        urlStr = 'https://blog.naver.com/PostView.nhn?blogId=%s&logNo=%s&redirect=Dlog&widgetTypeCall=true&directAccess=false' % (
            idStr, noStr)
        return urlStr

def get_html(url):
        #####엑셀관련코드추가#####
        err = 0
        while err < 5:
            try:
                r = requests.get(url)
                if r.status_code == requests.codes.ok:
                    t = r.text
                    t = re.sub('<p', '\n<p', t, 0, re.I | re.S)
                    t = re.sub('<br>', '\n<br>', t, 0, re.I | re.S)
                    return t
                else:
                    pass
            except :
                pass
            print("cannot access. waiting 4min for re-entry")
            sleep(240)

def get_text(soup):
        bodySoup = soup.find_all('div', {'class': 'se-main-container'})
        if (len(bodySoup) == 0):
            bodySoup = soup.find_all('div', {'class': 'se_paragraph'})
        if (len(bodySoup) == 0):
            bodySoup = soup.find_all('div', {'id': 'postViewArea'})
        text = ''
        for bs in bodySoup:
            text += bs.getText()
        text = cleanse(text)
        return text

def crawl():
    crawl_task.update_one({'_id': task_id}, {"$set": {'crawl_status': status_doing}})
    custom_header = CUSTOM_HEADER
    custom_header['referer']+=keyhex
    nTotal = 0
    num = 0
    pageNo = 1
    ban_counter = 0
    err = 0
    end = False

    while num < n_crawl:
        list_url = "https://section.blog.naver.com/ajax/SearchList.nhn?countPerPage=7&currentPage=%d&endDate=%s" % (
            pageNo, to_date) + "&keyword=%s&orderBy=sim&startDate=%s&type=post" % (keyhex, from_date)
        print(num, n_crawl, 'crawling - get list', list_url, )

        req = requests.get(list_url, headers=custom_header)  # custom_header를 사용하지 않으면 접근 불가
        if req.status_code == requests.codes.ok:
            r = req.text[6:]
            data_all = json.loads(r)

            ### task_log 입력
            if num == 0:
                nTotal = data_all['result']['totalCount']
                print(nTotal, 'items found for ' + keyword)
            data_list = []
            try:
                data_list = data_all['result']['searchList']
            except Exception as ex:
                print(ex)

            if len(data_list) < 7:
                print(f"N of files : {len(data_list)}")
                print("Process will be ended")
                end = True

            if num >= nTotal:
                print(f"전체 게시물을 모두 읽어왔습니다 : {num}")
                print(f"Process complete. crawled files : {num}")
                crawl_task.update_one({'_id': task_id}, {"$set": {'crawl_status': status_done}})
                break

            for data in data_list:
                num += 1
                try:
                    url = get_realUrl(data['blogId'], data['logNo'])
                    print('crawling', num, url)
                    post_date = dt.fromtimestamp(data['addDate'] / 1e3).strftime("%Y-%m-%d")
                    title = data['noTagTitle']
                    author = f"{data['nickName']}({data['blogName']})"
                    soup = BeautifulSoup(get_html(url), 'html.parser')
                    text = get_text(soup)


                    contents_insert_dict = {
                        "task_id":task_id,
                        "num":num,
                        "post_date":post_date,
                        "title":title,
                        "text":text,
                        "author":author,
                        "url":url,
                        "task_datetime":task_datetime
                    }
                    crawl_contents.insert_one(
                        contents_insert_dict
                    )
                except Exception as ex:
                    print(ex)

                if ban_counter >= 2500:
                    sleep(120)
                    ban_counter = 0
                if num >= n_crawl:

                    crawl_task.update_one({'_id': task_id}, {"$set": {'n_crawled': num}})
                    crawl_task.update_one({'_id': task_id}, {"$set": {'crawl_status': status_done}})

                    print(f"Process complete. crawled files : {num}")
                    break
            pageNo += 1


        else:
            err += 1
            print("request error:" + str(err))
            print("waiting 4min for re-entry")
            sleep(240)
            if err > 5:
                print("Process ended by error")
                end = True

        if end:
            crawl_task.update_one({'_id': task_id}, {"$set": {'n_crawled': num}})
            crawl_task.update_one({'_id': task_id}, {"$set": {'crawl_status': status_done}})
            break

        crawl_task.update_one({'_id': task_id}, {"$set": {'n_crawled': num}})

crawl_total()
crawl()
