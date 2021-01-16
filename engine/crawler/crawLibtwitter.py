from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pychrome
import time
import json
from urllib.parse import urlsplit, parse_qs
import requests
import pymysql
import re
headers = {
    'authority': 'api.twitter.com',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'x-twitter-client-language': 'ko',
    'x-csrf-token': 'afd798f6faa8439681a24cd0de6d29cd',
    'x-guest-token': '1334439552904126468',
    'x-twitter-active-user': 'yes',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://twitter.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://twitter.com/search?q=%EA%B0%80%EB%8D%95%EB%8F%84%20%EC%8B%A0%EA%B3%B5%ED%95%AD%20until%3A2016-01-31%20since%3A2016-01-01&src=typed_query&f=live',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'personalization_id="v1_R+6nzbekPREd9Rf3m3cZtw=="; guest_id=v1%3A160699015574430454; ct0=afd798f6faa8439681a24cd0de6d29cd; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLLTEyh2AToMY3NyZl9p%250AZCIlZGQxN2YxMmFkMmU1ZTFmYzJmYWRhZTgyYWQxNjE1ZjA6B2lkIiU4MGY2%250AMGUzMzhiOWY1NWYxZmI1Y2Q2M2FiYTJlOGE5Ng%253D%253D--d5dcbf9cd350b284b66c28dce2bc5e625e4f9328; gt=1334439552904126468; _ga=GA1.2.1033852213.1606990158; _gid=GA1.2.1941420322.1606990158',
}




class CrawlLibTwitter:

    def __init__(self,search_key, channel,startDate, endDate, nCrawl):
        self.PARAMS = (
            ('include_profile_interstitial_type', '1'),
            ('include_blocking', '1'),
            ('include_blocked_by', '1'),
            ('include_followed_by', '1'),
            ('include_want_retweets', '1'),
            ('include_mute_edge', '1'),
            ('include_can_dm', '1'),
            ('include_can_media_tag', '1'),
            ('skip_status', '1'),
            ('cards_platform', 'Web-12'),
            ('include_cards', '1'),
            ('include_ext_alt_text', 'true'),
            ('include_quote_count', 'true'),
            ('include_reply_count', '1'),
            ('tweet_mode', 'extended'),
            ('include_entities', 'true'),
            ('include_user_entities', 'true'),
            ('include_ext_media_color', 'true'),
            ('include_ext_media_availability', 'true'),
            ('send_error_codes', 'true'),
            ('simple_quoted_tweet', 'true'),
            ('q', '{} until:{} since:{}'.format(search_key,endDate,startDate)),
            ('tweet_search_mode', 'live'),
            ('count', '20'),
            ('query_source', 'typed_query'),
            ('pc', '1'),
            ('spelling_corrections', '1'),
            ('ext', 'mediaStats,highlightedLabel'),
        )
        self.search_key = search_key
        self.channel = channel
        self.startDate = startDate
        self.endDate = endDate
        self.nCrawl = nCrawl
        self.listen_target_url = 'https://twitter.com/search?q={}&src=recent_search_click&f=live'.format(search_key) if self.startDate=='0000-00-00' else \
            'https://twitter.com/search?q={}%20until%3A{}%20since%3A{}&src=typed_query&f=live'.format(self.search_key, self.endDate,self.startDate)
            # 'https://mobile.twitter.com/search?q=%EC%86%A1%EC%A0%84%ED%83%91%20until%3A2018-01-31%20since%3A2018-01-01&src=typed_query&f=live'
        self.conn = pymysql.connect(host='1.221.75.76', user='root', password='robot369',
                               db='dalmaden', charset='utf8mb4')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

        self.task_id = None
        self.CALLBACK_REQUEST_URL_LIST = []

    def cleanser(self,tweet_full_text):

        tweet_full_text= re.sub(u"(http[^ ]*)", " ", tweet_full_text)
        tweet_full_text = re.sub(u"@(.)*\s", " ", tweet_full_text)
        tweet_full_text = re.sub(u"#", "", tweet_full_text)
        tweet_full_text = re.sub(u"\\d+", " ", tweet_full_text)
        tweet_full_text = re.sub(u"[^가-힣A-Za-z]", " ", tweet_full_text)
        tweet_full_text = re.sub(u"\\s+", " ", tweet_full_text)

        return tweet_full_text
    def crawl(self):
        sql_insert_task_log = "insert into task_log (keyword,channel,startDate,endDate,nCrawl,nCrawled) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%d)" % \
                              (self.search_key, self.channel, self.startDate, self.endDate, self.nCrawl,0)

        self.curs.execute(sql_insert_task_log)
        self.task_id = self.curs.lastrowid
        self.conn.commit()

        driver = self.set_listener(self.listen_target_url)
        adaptive_url_list = self.get_adaptive_json_url(driver, self.nCrawl)
        self.get_tweets_list(adaptive_url_list)
        self.dev_tools.close_tab(tab_id=self.tab.id)
    def convert_date(self,date):
        date_date = date.split(' ')[2]
        date_year = date.split(' ')[5]
        date_month = date.split(' ')[1]
        date_month = date_month.replace("Jan","01")
        date_month = date_month.replace("Feb","02")
        date_month = date_month.replace("Mar","03")
        date_month = date_month.replace("Apr","04")
        date_month = date_month.replace("May","05")
        date_month = date_month.replace("Jun","06")
        date_month = date_month.replace("Jul","07")
        date_month = date_month.replace("Aug","08")
        date_month = date_month.replace("Sep","09")
        date_month = date_month.replace("Oct","10")
        date_month = date_month.replace("Nov","11")
        date_month = date_month.replace("Dec", "12")
        date = "%s-%s-%s"%(date_year,date_month,date_date)
        return date

    def output_on_start(self,**kwargs):

        self.CALLBACK_REQUEST_URL_LIST.append(kwargs['documentURL'])
        self.CALLBACK_REQUEST_URL_LIST.append(kwargs['request']['url'])
        return self.CALLBACK_REQUEST_URL_LIST

    def set_listener(self,listen_target_url):

        options = webdriver.ChromeOptions()
        options.add_argument("--remote-debugging-port=8000")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self.dev_tools = pychrome.Browser(url="http://localhost:8000")
        self.tab = self.dev_tools.list_tab()[0]
        self.tab.start()

        driver.get(listen_target_url)

        self.tab.call_method("Network.emulateNetworkConditions",offline=False,
                        latency=100,
                        downloadThroughput=93750,
                        uploadThroughput=31250,
                        connectionType="cellular3g")

        self.tab.call_method("Network.enable", _timeout=20)
        self.tab.set_listener("Network.requestWillBeSent", self.output_on_start)
        return driver

    def get_adaptive_json_url(self,driver,nCrawl):

        adaptive_url_list =[]
        conscious_cnt=0
        while True:
            ##스크롤 다운 이전의 url_list 개수를 샌다
            scroll_down_before_adaptive_url_list = len(adaptive_url_list)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            ##스크롤 다운 이후에 callback_request_url에 담겨진 url 개수를 가져온다
            adaptive_url_list = list(filter(lambda x: x.startswith('https://api.twitter.com/2/search/adaptive.json'), self.CALLBACK_REQUEST_URL_LIST))
            real_adaptive_url_list = list(set(adaptive_url_list))
            ##스크롤 다운 이전과 이후의 url 개수가 같으면 더이상 게시물이없다고 판단한다.
            if scroll_down_before_adaptive_url_list == len(adaptive_url_list):
                conscious_cnt +=1
            else :
                conscious_cnt=0
            ##없다고 판단을 10번 이상 하면 크롤러를 끝낸다.
            if conscious_cnt>10:
                print('no more data')
                break

            ##url 갯수는 한개당 대략 20개 정도의 트윗 데이터를 가지고 있음. 게시물 요청 갯수와 비교하여 커질때까지 계속한다
            while_condition = (len(adaptive_url_list) - 1) * 20 <= nCrawl

            ##긁어온 게시물이 더 많아지면 반복문을 그만한다.
            if while_condition == False:
                break
        time.sleep(1)

        return real_adaptive_url_list

    def get_tweets_full_text(self,tweets_data,task_id):
        nCrawled= 0
        for index,(tweet_id, tweet_data)  in enumerate(tweets_data.items()):
            try:
                tweet_created_date = self.convert_date(tweet_data['created_at'])
                tweet_full_text = tweet_data['full_text'].replace("\n",'')
                tweet_full_text = self.cleanser(tweet_full_text)
                if tweet_full_text.isspace():
                    continue
                print(index,tweet_created_date,tweet_full_text)
                nCrawled+=1

                ##insert 하기
                sql_insert_cdata = "insert into cdata (task_id,keyword,channel,post_date,text) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % \
                                      (task_id, self.search_key, 'twitter',tweet_created_date ,tweet_full_text)

                self.curs.execute(sql_insert_cdata)
                self.conn.commit()
            except Exception as e:
                print(e)
                continue
        return nCrawled

    def get_tweets_list(self,adaptive_url_list):
        total_nCrawled=0
        ##adaptive_url_list 에서 url 가져와서 해당 full text 추출하는 과정
        for adaptive_url in adaptive_url_list:
            adaptive_url_params = parse_qs(urlsplit(adaptive_url).query)
            PARAMS_DICT = dict(self.PARAMS)
            try:
                ##cursor id 를 가져와서 params_dict['cursor'] 에 넣어준다.
                PARAMS_DICT['cursor'] = adaptive_url_params['cursor']
                print("PARAMS_DICT['q']:",PARAMS_DICT['q'])
                ##tweet 본문내용이 들어있는 url로 request 하기
                response = requests.get('https://api.twitter.com/2/search/adaptive.json', headers=headers, params=PARAMS_DICT)
                # print(adaptive_url,response.status_code)
                adaptive_json = json.loads(response.text)

                ##1개의 tweets 에는 보통 20개의 tweet 데이터가 들어있음
                tweets_data = adaptive_json["globalObjects"]["tweets"]
                ##해당 url tweet 갯수 nCrawled 에 저장
                nCrawled = self.get_tweets_full_text(tweets_data,self.task_id)
                ##전체 url list 에 대한 tweet 갯수 total_nCrawled 에 저장
                total_nCrawled+=nCrawled
            except Exception as e:
                print(e)
        sql_update_task_log = 'update task_log set nCrawled=%s where id=%s'%(total_nCrawled,self.task_id)
        print(sql_update_task_log)
        self.curs.execute(sql_update_task_log)
        self.conn.commit()
        self.conn.close()

