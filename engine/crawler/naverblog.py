import requests
from bs4 import BeautifulSoup
import json
import pymysql
import re
from datetime import datetime
from time import sleep
import openpyxl
from almaden import Sql
from crawler_utils import cleanse

# custom_header을 통해 아닌 것 처럼 위장하기

CUSTOM_HEADER = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
    'referer': 'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword=',#+heyhex
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def crawl(keyword, startDate, endDate, nCrawl, comment="naverblog") :
    #init task
    db = Sql('dalmaden')

    keyhex = get_keyhex(keyword)
    custom_header = CUSTOM_HEADER
    custom_header['referer']+=keyhex

    num = 0
    pageNo = 1
    ban_counter = 0
    err = 0
    task_id = None
    end = False
    while num < nCrawl:
        list_url = "https://section.blog.naver.com/ajax/SearchList.nhn?countPerPage=7&currentPage=%d&endDate=%s" % (
            pageNo, endDate)+ "&keyword=%s&orderBy=sim&startDate=%s&type=post" % (keyhex, startDate)
        req = requests.get(list_url, headers=custom_header)  # custom_header를 사용하지 않으면 접근 불가
        if req.status_code == requests.codes.ok:
            r = req.text[6:]
            data_all = json.loads(r)

            ### task_log 입력
            if num == 0 :
                nTotal = data_all['result']['totalCount']
                print(nTotal, 'items found for ' + keyword)
                task_id = db.insert('task_log',
                          channel='naverblog',
                          keyword=keyword,
                          startDate=startDate,
                          endDate=endDate,
                          nTotal = nTotal,
                          nCrawl = nCrawl,
                          comment=comment)

            data_list = data_all['result']['searchList']

            if len(data_list) < 7:
                print("N of data : %d")%len(data_list)
                print("Process will be ended")
                end=True

            for data in data_list:
                num += 1
                if num % 100 == 0:
                    print('post Num :', num)
                try :
                    channel = 'naverblog'
                    url = get_realUrl(data['blogId'], data['logNo'])
                    post_date = datetime.fromtimestamp(data['addDate'] / 1e3).strftime("%Y-%m-%d")
                    title = data['noTagTitle']
                    author = f"{data['nickName']}({data['blogName']})"
                    soup = BeautifulSoup(get_html(url), 'html.parser')
                    text = get_text(soup)
                    db.insert('cdata',
                              task_id = task_id,
                              channel = channel,
                              keyword = keyword,
                              num = num,
                              post_date = post_date,
                              title = title,
                              text = text,
                              author = author,
                              url = url)
                except Exception as ex :
                    print(ex)

                if ban_counter >= 2500:
                    sleep(120)
                    ban_counter = 0
                if num >= nCrawl:
                    print(f"Process complete. crawled data : {num}")
                    end = True
                    break
            pageNo += 1


        else:
            err += 1
            print("request error:" + str(err))
            print("waiting 4min for re-entry")
            sleep(240)
            if err>5 :
                print("Process ended by error")
                end = True

        if end : break


def get_keyhex(keyword) :
    keyint = keyword.encode("UTF-8")
    keyhex = ""
    for i in keyint:
        keyhex = keyhex + '%{:02X}'.format(i)
    return keyhex

def get_realUrl(idStr, noStr):
    urlStr = 'https://blog.naver.com/PostView.nhn?blogId=%s&logNo=%s&redirect=Dlog&widgetTypeCall=true&directAccess=false' % (
        idStr, noStr)
    return urlStr

def get_html(url):
    print('crawling ', url)
    #####엑셀관련코드추가#####
    err = 0
    while err < 5 :
        try :
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
