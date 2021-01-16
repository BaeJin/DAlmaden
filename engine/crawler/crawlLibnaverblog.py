import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime as dt
from time import sleep
from engine.sql.almaden import Sql
from engine.sql.almaden import cleanse


class CrawlLibnaverBlog:

    def __init__(self,task_id,keyword, from_date, to_date, n_crawl=None,n_total=None):
        self.task_id = task_id
        self.status_done = 'GF'
        self.status_doing = 'GI'
        self.status_do = 'GR'
        self.status_error = 'ER'
        self.keyword = keyword
        self.startDate = from_date
        self.endDate = to_date
        self.nCrawl = n_crawl
        self.nTotal = n_total
        self.CUSTOM_HEADER ={'accept': 'application/json, text/plain, */*',
                            'accept-encoding': 'gzip, deflate, br',
                            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                            'cookie': 'NNB=26JKENAB5VNFY; npic=LW1n/Y7lr1485twRJiDAu7IQNma7Byg1+eD1dujBnEarfw1Jj92XPcGCQrmTmIkDCA==; _ga=GA1.2.785938604.1550973896; nx_ssl=2; BMR=; _naver_usersession_=ldZTind9DyvToDWTHUQkNw==; page_uid=UfWJIwprvOsssOBmEzdssssstul-404192; JSESSIONID=FE270C9B4B35C84D83479B52E6020831.jvm1',
                            'referer': 'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword=',#+heyhex
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    def crawl_total(self):
        db = Sql('datacast2')

        keyhex = self.get_keyhex(self.keyword)
        custom_header = self.CUSTOM_HEADER
        custom_header['referer'] += keyhex
        pageNo = 1
        list_url = "https://section.blog.naver.com/ajax/SearchList.nhn?countPerPage=7&currentPage=%d&endDate=%s" % (
            pageNo, self.endDate) + "&keyword=%s&orderBy=sim&startDate=%s&type=post" % (keyhex, self.startDate)

        req = requests.get(list_url, headers=custom_header)  # custom_header를 사용하지 않으면 접근 불가
        if req.status_code == requests.codes.ok:
            r = req.text[6:]
            data_all = json.loads(r)

            ### task_log 입력
            nTotal = data_all['result']['totalCount']
            print(nTotal, 'items found for ' + self.keyword,self.task_id)
            db.update_one('crawl_task', 'n_total', int(nTotal), 'task_id', self.task_id)

    def crawl(self):
        #init task
        db = Sql('datacast2')

        keyhex = self.get_keyhex(self.keyword)
        custom_header = self.CUSTOM_HEADER
        custom_header['referer']+=keyhex
        nTotal = 0
        num = 0
        pageNo = 1
        ban_counter = 0
        err = 0
        end = False
        while num < self.nCrawl:
            list_url = "https://section.blog.naver.com/ajax/SearchList.nhn?countPerPage=7&currentPage=%d&endDate=%s" % (
                pageNo, self.endDate)+ "&keyword=%s&orderBy=sim&startDate=%s&type=post" % (keyhex, self.startDate)
            print(num,self.nCrawl,'crawling - get list',list_url, )

            req = requests.get(list_url, headers=custom_header)  # custom_header를 사용하지 않으면 접근 불가
            if req.status_code == requests.codes.ok:
                r = req.text[6:]
                data_all = json.loads(r)

                ### task_log 입력
                if num == 0 :
                    nTotal = data_all['result']['totalCount']
                    print(nTotal, 'items found for ' + self.keyword)
                    db.update_one('crawl_task','crawl_status','%s'%(self.status_doing),'task_id',self.task_id)

                data_list = []
                try :
                    data_list = data_all['result']['searchList']
                except Exception as ex :
                    print(ex)

                if len(data_list) < 7:
                    print(f"N of files : {len(data_list)}")
                    print("Process will be ended")
                    end = True

                if num >= nTotal:
                    print(f"전체 게시물을 모두 읽어왔습니다 : {num}")
                    print(f"Process complete. crawled files : {num}")
                    db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_done), 'task_id', self.task_id)
                    break


                for data in data_list:
                    num += 1
                    try:
                        url = self.get_realUrl(data['blogId'], data['logNo'])
                        print('crawling',num, url)
                        post_date = dt.fromtimestamp(data['addDate'] / 1e3).strftime("%Y-%m-%d")
                        title = data['noTagTitle']
                        author = f"{data['nickName']}({data['blogName']})"
                        soup = BeautifulSoup(self.get_html(url), 'html.parser')
                        text = self.get_text(soup)
                        db.insert('crawl_contents',
                                  task_id = self.task_id,
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
                    if num >= self.nCrawl:
                        db.update_one('crawl_task', 'n_crawled', num, 'task_id', self.task_id)
                        db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_done), 'task_id',
                                      self.task_id)

                        print(f"Process complete. crawled files : {num}")
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

            if end :
                db.update_one('crawl_task', 'n_crawled', num , 'task_id', self.task_id)
                db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_done), 'task_id', self.task_id)

                break
            db.update_one('crawl_task','n_crawled',num,'task_id',self.task_id)

    def get_keyhex(self,keyword) :
        keyint = keyword.encode("UTF-8")
        keyhex = ""
        for i in keyint:
            keyhex = keyhex + '%{:02X}'.format(i)
        return keyhex

    def get_realUrl(self,idStr, noStr):
        urlStr = 'https://blog.naver.com/PostView.nhn?blogId=%s&logNo=%s&redirect=Dlog&widgetTypeCall=true&directAccess=false' % (
            idStr, noStr)
        return urlStr

    def get_html(self,url):
        #####엑셀관련코드추가#####
        err = 0
        while err < 5 :
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


    def get_text(self,soup):
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
