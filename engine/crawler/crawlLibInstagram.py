import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urlencode
from engine.sql.almaden import Sql
from engine.preprocess.calcDate import DateCalculator
import unicodedata
import sys
sys.setrecursionlimit(4000)

# HASH_KEY = "graphql"
# HASHTAG_KEY = "hashtag"
# MEDIA_KEY = "edge_hashtag_to_media"
# LIST_KEY = "edges"
# NODE_KEY = "node"
# CAPTION_LIST_KEY = "edge_media_to_caption"
# TEXT_KEY = "text"
# COUNT_KEY = "count"
API_KEY = "XAZN5Y277PEU020TOQWCSZL8PXCM3AKBZPXTX67S6ZBO7Y7QXC9WTV0T7O2EK4QRWR0O2I3Z0F0EM92X"


class CrawlLibInstagram:
    def __init__(self, task_id=None, keyword=None,from_date=None,to_date=None,n_crawl=None,n_total=None,need_reply:bool = True,get_nTotal: bool = False):
        self.status_done = 'GF'
        self.status_doing = 'GI'
        self.status_do = 'GR'
        self.status_error = 'ER'
        self.db = Sql('datacast2')
        self.comment_author = None
        self.task_id = task_id
        self.keyword = keyword.replace(" ", "")
        self.n_crawl = n_crawl
        self.n_crawled = 0
        self.nTotal = n_total
        self.get_nTotal = get_nTotal
        self.need_reply = need_reply
        self.dateCalc_obj = DateCalculator()
        # 유저이름에 대한 contents 검색 https://www.instagram.com/<user_name>/
        # https://www.instagram.com/explore/locations/<location_id>
        # Tags URL
        # 나라 설정은 parameter : hl 이용 ex)https://www.instagram.com/nike/?hl=en  #English
        self.instagram_target_url = f'https://www.instagram.com/explore/tags/{self.keyword}'
        self.scrapi_url = f"https://api.proxycrawl.com?token={API_KEY}"
        self.start_url = f"{self.scrapi_url}&url={self.instagram_target_url}"
        self.crawl_total_try_num = 0
        self.get_request_response_try_num = 0
        self.response_fail_count = 0
        self.MAX_TRY_NUM = 4
        self.headers = {
            'authority': 'www.instagram.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'ig_did=D9D44D70-785A-4814-AB46-74BF1F07B559; mid=X6p_dwABAAGYG0nisEzSR9hUS2dd; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; shbid=17829; shbts=1608544334.6645594; rur=ATN; csrftoken=O2dXN1Fq0AhBt8K7uqGcAHjsVfmW2MXa; ds_user_id=4972296107; sessionid=4972296107^%^3A8h0QqdwUREOpzx^%^3A8; fbsr_124024574287414=EJGUTvIc_LCO-Gk2-sW8srGpIL078QFbMX5qIVQIHWc.eyJ1c2VyX2lkIjoiMTAwMDAzMjYyMzE0MjQ4IiwiY29kZSI6IkFRQWgxcjRWcktUeUFqS2NKaXc5cmF6a0taNE0yNFgzSGx4OGJKeWlNaHA0RTBUWXVzSkprLVB0NUc3ZjJsRkhFS3JjY3FMeDd5RUFGdk42ZkpHY2M4Z0dtVmx4Ql9ZakVMTXNhR3BBRnFQRnJrRE1uSU5Zb1NzNC1GenM2VlpraDNBUzlWdmU1OG5JMUY4UWFXazVqQ085VnNLMm5MUFhpalBFSXVHbjNPNklxV3FzbVFBaXpKcjVYR1IzcFBpY2prbTRuSzdNOWxraVNhT1ppbHhvMHRSUmFKZmE2ODZMNXdFZzJFRXA4OTR4SWxVNGhybm5VX2xIVzdEcE40Y1hIZERfdno1SVlYZ1BJaWtCeVZRWjE0SmVLZFdHeDk0VzFRWkg2WUYzejV5NTJhR0VUalROT1JuaERmOHRMSlNsWTVhaTF3MjNJN1pHaWhhVy1CWGpOSjdDIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUJ5ZWNZa1VkSkM3eGpnSG9DbkpKcGNBTUdlSDdNV04yR01BdzROYWdaQVRyeDRSOXdZdjZmcXlSUjN6dmFUNkxTZjRhZmwyODBjOVRWUXN1UkhJSHNjSThaQjdCRXdUWWhmQkdJcnFnR28zdG5zUEpPcUNHUURBbmV2VktuNHBBeUtCcEo0WkJXeUJtY0U3TXd0MlM4dVZmVFRPTVpCWkFTRE9Ob3RNWkMiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYwODU0NTQzNH0; urlgen=^\\^^{^\\^\\^\\^1.221.75.76^\\^\\^\\^:',
        }

    def get_url(self, instagram_target_url):
        url = f"https://app.scrapingbee.com/api/v1/?api_key={API_KEY}&url={instagram_target_url}"
        print("scrapi_url:",url)
        return url

    def send_request(self, instagram_target_url):
        response = requests.get(
            url="https://app.scrapingbee.com/api/v1/",
            params={
                "api_key": "XAZN5Y277PEU020TOQWCSZL8PXCM3AKBZPXTX67S6ZBO7Y7QXC9WTV0T7O2EK4QRWR0O2I3Z0F0EM92X",
                "url": instagram_target_url,
                "render_js": "false",
            },
        )
        return response
    def get_request_response_to_crawl_total(self, instagram_target_url):
        self.get_request_response_try_num += 1
        response = self.send_request(instagram_target_url)
        soup = BeautifulSoup(response.text, 'lxml')
        result_exist = soup.find('title', text=re.compile("Instagram"))
        result_target_exist = soup.find('title', text=re.compile(self.keyword))

        # result 가 있을때
        if result_exist:
            # result 가 있고 taget 이 있으면
            if result_target_exist:
                print(self.instagram_target_url, "result exist and target exist")
                return response

            # target 이 없으면
            else:
                print(self.instagram_target_url, "result exist and target not exist")
                self.db.update_one('crawl_task', 'n_total', 0, 'task_id', self.task_id)
                return False

        # result 가 없을때
        elif not result_exist:
            # request 가 실패할 가능성이 있기 때문에 4번정도 시도해본다.
            if self.get_request_response_try_num <= self.MAX_TRY_NUM:
                print(self.instagram_target_url,
                      f"result not exist it maybe request error"
                      f" we try{self.MAX_TRY_NUM - self.get_request_response_try_num} times more")

                self.db.update_one('crawl_task', 'n_total', 0, 'task_id', self.task_id)
                return self.get_request_response_to_crawl_total(instagram_target_url)
            ## 4번이상 request 가 실패한 경우 error 처리를 해준다.
            else:
                print(self.instagram_target_url, "result not exist")
                self.db.update_one('crawl_task', 'n_total', -1, 'task_id', self.task_id)
                return False

    def crawl_total(self):
        response = self.get_request_response_to_crawl_total(self.instagram_target_url)
        if response:
            try:
                self.crawl_total_try_num += 1
                ##1. 받아온 데이터 parsing 작업
                response_html = response.text
                soup = BeautifulSoup(response_html, 'lxml')

                ##window._sharedDate 의 내용만 가져오기
                source_page_soup = soup.find('script', text=re.compile("window._sharedData = ")).string
                source_page_soup = str(source_page_soup)
                json_string = source_page_soup.strip().replace("window._sharedData = ", "")
                json_string = json_string.replace(";", "")

                ##가져온 data 를 json 형태로 parsing
                data = json.loads(json_string)
                # hashtag_id = data['entry_data']['TagPage'][0]['graphql']['hashtag']['id']

                ##해당 페이지에 대한 정보 가져오는 작업
                ##nTotal 만 가져올 경우 self.get_nTotal = True 갯수만 가져오고 return 한다.
                nTotal = \
                    data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
                self.db.update_one('crawl_task', 'n_total', nTotal, 'task_id', self.task_id)
                self.crawl_total_try_num = 0
            except Exception as e:
                if self.crawl_total_try_num > 3:
                    self.db.update_one('crawl_task', 'n_total', -1, 'task_id', self.task_id)
                    print("crawl_total:", e)
                elif self.crawl_total_try_num <= 3:
                    self.crawl_total()

    def get_content(self, edge):
        captions = ""  # 내용
        if edge['node']['edge_media_to_caption']:
            for edge_caption in edge['node']['edge_media_to_caption']['edges']:
                captions += edge_caption['node']['text'] + "\n"
        captions = unicodedata.normalize('NFC', captions)
        return captions

    def get_reply(self, edge):

        url = 'https://www.imginn.com/p/' + edge['node']['shortcode']
        res = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')
        comment_author = soup.find('div', {'class': 'username'})
        comment_author = comment_author.get_text() if comment_author is not None else ''
        comment_author = comment_author[1:-1]
        self.comment_author = comment_author
        if soup.find_all('div', {'class': 'comment'}) is not None:
            reply_list = []
            for idx, el in enumerate(soup.find_all('div', {'class': 'comment'})):
                sentence_post_time = self.dateCalc_obj.calcDatetime(datetime.now(),
                                                                    el.find('span', {'class': 'time'}).get_text()
                                                                    if el.find('span', {
                                                                        'class': 'time'}).get_text() is not None else datetime.now())
                sentence_post_date = sentence_post_time.date()
                author = el.find('h2').get_text() if el.find('h2').get_text() is not None else ''
                comment = el.find('p').get_text() if el.find('p').get_text() is not None else ''

                reply = {'order': idx,
                         'author': author,
                         'sentence_post_time': sentence_post_time,
                         'sentence_post_date': sentence_post_date,
                         'comment': comment}
                reply_list.append(reply)
            return reply_list

    def start_requests(self):
        self.db.update_one('crawl_task','crawl_status',self.status_doing,'task_id',self.task_id)
        response = self.send_request(self.instagram_target_url)
        if response.status_code == 200:
            print(self.start_url, "start_requests requests success")
            self.parse(response)
        else:
            print(self.start_url, "start_requests requests failure")
            self.start_requests()

    def parse(self, response):
        try:
            ##1. 받아온 데이터 parsing 작업
            response_html = response.text
            soup = BeautifulSoup(response_html, 'lxml')

            ##window._sharedDate 의 내용만 가져오기
            source_page_soup = soup.find('script', text=re.compile("window._sharedData = ")).string
            source_page_soup = str(source_page_soup)
            json_string = source_page_soup.strip().replace("window._sharedData = ", "")
            json_string = json_string.replace(";", "")

            ##가져온 data 를 json 형태로 parsing
            data = json.loads(json_string)
            # hashtag_id = data['entry_data']['TagPage'][0]['graphql']['hashtag']['id']

            ##해당 페이지에 대한 정보 가져오는 작업

            ##netx_page 있는지 확인 next_page_bool : bool
            next_page_bool = \
                data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                    'has_next_page']

            ##page 의 contents 정보 가져오기
            edges = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']

            for edge_index, edge in enumerate(edges):
                url = 'https://www.instagram.com/p/' + edge['node']['shortcode']  # 게시물 url
                video = edge['node']['is_video']  # 비디오 있는지 확인
                date_posted_timestamp = edge['node']['taken_at_timestamp']
                date_posted = datetime.fromtimestamp(date_posted_timestamp).strftime("%Y/%m/%d")
                datetime_posted = datetime.fromtimestamp(date_posted_timestamp).strftime("%Y/%m/%d %H:%M:%S")  # 게시물 업데이트 시간
                like_count = edge['node']['edge_media_preview_like']['count'] if "edge_media_preview_like" in edge[
                    # 좋아요 수
                    'node'].keys() else ''
                comment_count = edge['node']['edge_media_to_comment']['count'] if 'edge_media_to_comment' in edge[
                    # 댓글 수
                    'node'].keys() else ''

                # 내용
                captions = self.get_content(edge)

                # 댓글

                reply = self.get_reply(edge) if self.need_reply else None

                if video:
                    image_url = edge['node']['display_url']
                else:
                    image_url = edge['node']['thumbnail_resources'][-1]['src']  # 이미지 저장
                print(edge_index, video, url)
                # print(url, date_posted_human, like_count, comment_count,image_url )

                # item = {'postURL': url, 'isVideo': video, 'date_posted': date_posted,
                #         'datetime_posted': datetime_posted, 'likeCount': like_count, 'commentCount': comment_count,
                #         'image_url': image_url,
                #         'captions': captions[:-1],
                #         'replys': reply}

                self.db.insert('crawl_contents',
                               url=url,
                               task_id=self.task_id,
                               num=self.n_crawled,
                               text=captions[:-1],
                               author=self.comment_author,
                               post_date=date_posted,
                               post_time=datetime_posted,
                               n_reply=comment_count,
                               n_like=like_count,
                               img_url=image_url)

                self.n_crawled += 1
                self.db.update_one('crawl_task','n_crawled',self.n_crawled,'task_id',self.task_id)
                self.comment_author = None
                # print(item)

            ##현재 페이지에 대한 모든 콘텐츠 크롤링이 끝남
            ##다음 페이지 있는지 확인 있으면 해당 작업을 반복한다.
            ##다음 페이지로 넘어가기 위해서는 현재 페이지에서 다음 페이지에 대한 cursr 정보를 가져와야함
            if next_page_bool:
                cursor = \
                    data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                        'end_cursor']
                next_page_di = {'tag_name': self.keyword, 'first': 20, 'after': cursor}
                params = {'query_hash': '9b498c08113f1e09617a1703c22b2f32', 'variables': json.dumps(next_page_di)}
                instagram_target_url = 'https://www.instagram.com/graphql/query/?' + urlencode(params)

                return self.parse_page(self.send_request(instagram_target_url),next_page_di,instagram_target_url=instagram_target_url)

            elif next_page_bool is False:
                print(f'총 게시물 수 {self.nTotal} 더이상 게시물이 없습니다.')
                self.db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_done), 'task_id', self.task_id)
                return

        except Exception as e:
            self.db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_error), 'task_id', self.task_id)
            print(e, 'parse_error')
        # print('start_request and start parse success now we start iterating page')

    def parse_page(self, response, di,instagram_target_url=None):
        self.response_fail_count = 0
        while self.n_crawled <= min(self.n_crawl,self.nTotal):
            try:
                json_string = response.text
                data = json.loads(json_string)
                # hashtag_id = data['entry_data']['TagPage'][0]['graphql']['hashtag']['id']

                next_page_bool = \
                    data['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']

                edges = data['data']['hashtag']['edge_hashtag_to_media']['edges']

            except Exception as e:
                print("parse page error:", e)
                response_success = True
                while response_success == True:
                    response = self.send_request(instagram_target_url)
                    print(self.n_crawled, response.status_code)
                    if response.status_code == 200:
                        return self.parse_page(response, di)
                    else:
                        self.response_fail_count += 1
                        if self.response_fail_count >= 5:
                            print('error is occured','response_fail_count:',self.response_fail_count)
                            self.db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_error),
                                               'task_id', self.task_id)
                            break
                break

            for edge_index, edge in enumerate(edges):
                url = 'https://www.instagram.com/p/' + edge['node']['shortcode']
                video = edge['node']['is_video']
                date_posted_timestamp = edge['node']['taken_at_timestamp']
                date_posted = datetime.fromtimestamp(date_posted_timestamp).strftime("%Y/%m/%d")
                datetime_posted = datetime.fromtimestamp(date_posted_timestamp).strftime("%Y/%m/%d %H:%M:%S")  # 게시물 업데이트 시간

                like_count = edge['node']['edge_media_preview_like']['count'] if "edge_media_preview_like" in edge[
                    'node'].keys() else ''
                comment_count = edge['node']['edge_media_to_comment']['count'] if 'edge_media_to_comment' in edge[
                    'node'].keys() else ''

                # 내용
                captions = self.get_content(edge)

                # 댓글
                reply = self.get_reply(edge) if self.need_reply else None

                if video:
                    image_url = edge['node']['display_url']
                else:
                    image_url = edge['node']['thumbnail_resources'][-1]['src']
                print(edge_index, video, url)
                # item = {'postURL': url, 'isVideo': video, 'date_posted': date_posted,
                #         'datetime_posted': datetime_posted, 'likeCount': like_count, 'commentCount': comment_count,
                #         'image_url': image_url,
                #         'captions': captions[:-1],
                #         'replys': reply}

                self.db.insert('crawl_contents',
                               url=url,
                               task_id=self.task_id,
                               num =self.n_crawled,
                               text=captions[:-1],
                               author=self.comment_author,
                               post_date=date_posted,
                               post_time=datetime_posted,
                               n_reply=comment_count,
                               n_like=like_count,
                               img_url=image_url)

                self.n_crawled += 1
                self.db.update_one('crawl_task', 'n_crawled', self.n_crawled, 'task_id', self.task_id)
                self.comment_author = None
            if next_page_bool:
                cursor = \
                    data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']

                ##cursor 를 업데이트
                di['after'] = cursor
                params = {'query_hash': '9b498c08113f1e09617a1703c22b2f32', 'variables': json.dumps(di)}
                instagram_target_url = 'https://www.instagram.com/graphql/query/?' + urlencode(params)

                # 다음 페이지가 없을 때 까지 n_crawl 보다 작을 때 까지 반복한다.

                if self.n_crawled <= min(self.n_crawl,self.nTotal):
                    response_success = True
                    response_fail_count = 0
                    while response_success == True:
                        response = self.send_request(instagram_target_url)
                        print(self.n_crawled, response.status_code)
                        if response.status_code == 200:
                            return self.parse_page(response, di,instagram_target_url=instagram_target_url)
                        else:
                            response_fail_count += 1
                            if response_fail_count >= 5:
                                print('error is occured','response_fail_count:',response_fail_count)
                                self.db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_error),
                                                   'task_id', self.task_id)
                                return
            else:
                print(f'총 게시물 수 {self.nTotal} 개를 크롤링 하였습니다. 더이상 게시물이 없습니다.')
                self.db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_done), 'task_id',self.task_id)
                break

            self.db.update_one('crawl_task', 'crawl_status', '%s' % (self.status_done),
                               'task_id', self.task_id)