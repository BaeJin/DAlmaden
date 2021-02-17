from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from bs4 import BeautifulSoup
from html import unescape
import re
from engine.sql.almaden import Sql
from sqlalchemy import create_engine
import json
from youtube.source.account import accounts

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class CrawlLibYoutube:

    def __init__(self,task_id=None,
                 contents_id=None,
                 keyword=None,
                 n_total=None,
                 prod_desc=None,
                 cate_id = None,
                 is_channel = None,
                 default_product_num=50):

        self.engine = create_engine(("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8").format('root','robot369','1.221.75.76',3306,'datacast'),encoding='utf-8')
        self.db = Sql("datacast2")
        self.task_id = task_id
        self.contents_id = contents_id
        self.keyword = keyword
        self.n_total = n_total
        self.prod_desc = prod_desc
        self.channel = 'youtube'
        self.default_product_num = default_product_num
        self.n_crawled = 0
        self.cate_id = cate_id
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey="AIzaSyAViOEVGzy-FigDtvCw3rvfOu678wOUq7I")
        self.is_channel = is_channel
    def convert_named_character(self,text):

        _charref = re.compile(r'&(#[0-9]+;?'
                               r'|#[xX][0-9a-fA-F]+;?'
                               r'|[^\t\n\f <&#;]{1,32};?)')

        text = _charref.sub('', text)
        return text

    def search_request_by_keyword(self):
        ##전체 유튜브 동영상 갯수 입력하기
        search_response = self.youtube.search().list(
            q=self.keyword,
            order="viewCount",
            part="id,snippet",
            maxResults=50,
            type="video").execute()
        return search_response

    def search_request_by_channel(self):
        channels = []
        ##전체 유튜브 동영상 갯수 입력하기
        search_response = self.youtube.search().list(
            q=self.keyword,
            order="viewCount",
            part="id,snippet",
            maxResults=50,
            type="channel").execute()

        for idx, search_result in enumerate(search_response.get("items")):
            if search_result["snippet"]["title"].lower() == self.keyword:
                channel_id = search_result["id"]["channelId"]
                channels.append(channel_id)

        channel_id = channels[0]
        search_response = self.youtube.search().list(
            channelId=channel_id,
            order="viewCount",
            part="id,snippet",
            maxResults=50,
            type="video").execute()
        return search_response

    def get_video_more_info(self,video_id):
        ##전체 유튜브 동영상 갯수 입력하기
        search_response = self.youtube.videos().list(
            id=video_id, part='statistics'
        ).execute()
        views = search_response['items'][0]['statistics']['viewCount'] if 'viewCount' in search_response['items'][0]['statistics'].keys() else None
        likes = search_response['items'][0]['statistics']['likeCount'] if 'likeCount' in search_response['items'][0]['statistics'].keys() else None
        dislikes = search_response['items'][0]['statistics']['dislikeCount'] if 'dislikeCount' in search_response['items'][0]['statistics'].keys() else None
        comments = search_response['items'][0]['statistics']['commentCount'] if 'commentCount' in search_response['items'][0]['statistics'].keys() else None

        get_video_more_info_dict = {'n_view':views, 'n_like':likes, 'n_dislike':dislikes, 'n_reply':comments}
        return get_video_more_info_dict

    def crawl_total(self):
        db = Sql("datacast2")
        request = db.select('crawl_request AS cr '
                            'JOIN crawl_request_task AS crt ON cr.request_id= crt.request_id '
                            'JOIN crawl_task AS ct ON ct.task_id = crt.task_id', what='cr.category_id,ct.is_channel',
                            where=f'ct.task_id={self.task_id}')
        print("task_id:",self.task_id)
        self.cate_id = request[0]['category_id'] if request[0]['category_id'] is not None else None

        if self.is_channel == 0:
            print("is_channel", 0)
            search_response = self.search_request_by_keyword()

        elif self.is_channel == 1:
            print("is_channel",1)
            search_response = self.search_request_by_channel()
        else:
            print("is_channel", "else")
            search_response = self.search_request_by_keyword()

        self.crawl_total_content_count(search_response)
        self.crawl_content_list(search_response)

    def crawl_total_content_count(self,search_response):
        nTotal = search_response['pageInfo']['totalResults']
        self.db.update_one('crawl_task', 'n_total', int(nTotal), 'task_id', self.task_id)

    def crawl_content_list(self,search_response):

        for idx, search_result in enumerate(search_response.get("items")):
            print(search_result)
            if search_result["id"]["kind"] == "youtube#video":
                video_id = search_result["id"]["videoId"]
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                video_detail = self.get_video_more_info(video_id)
                title = unescape(search_result["snippet"]["title"])
                post_date = search_result["snippet"]["publishedAt"].split("T")[0]
                # description = unescape(search_result["snippet"]["description"])
                thumbnails = search_result["snippet"]["thumbnails"]["default"]["url"]
                text_memo = search_result
                text_memo['statics'] = video_detail
                self.db.insert('crawl_contents',
                               title = title,
                               url = video_url,
                               product_name = title,
                               task_id = float(self.task_id),
                               text = json.dumps(text_memo),
                               post_date=post_date,
                               img_url = thumbnails,
                               n_view = video_detail['n_view'],
                               n_reply=video_detail['n_reply'],
                               n_like=video_detail['n_like'],
                               n_dislike=video_detail['n_dislike'],
                               crawl_status='GR'
                               )
    def crawl(self,part='snippet',maxResults=100,textFormat='plainText',order='time'):
        video_info = self.prod_desc
        videoId = video_info['id']['videoId']

        n_reply_crawled = 0
        response = self.youtube.commentThreads().list(
            part=part,
            maxResults=maxResults,
            textFormat=textFormat,
            order=order,
            videoId=videoId).execute()
        while response:  # this loop will continue to run until you max out your quota
            for item in response['items']:
                # item for desired data features
                n_reply_crawled+=1
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_id = item['snippet']['topLevelComment']['id']
                # reply_count = item['snippet']['totalReplyCount']
                like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
                post_date = item['snippet']['topLevelComment']['snippet']['publishedAt'].split("T")[0]

                self.db.insert("crawl_sentence",
                               seq=n_reply_crawled,
                               contents_id = self.contents_id,
                               text=comment,
                               author=comment_id,
                               sentence_post_date=post_date,
                               n_like = like_count)
                self.db.update_one("crawl_contents", "n_reply_crawled", n_reply_crawled, "contents_id", self.contents_id)
            # check for nextPageToken, and if it not exists break
            if 'nextPageToken' in response:
                response = self.youtube.commentThreads().list(
                    part=part,
                    maxResults=maxResults,
                    textFormat=textFormat,
                    order=order,
                    videoId=videoId,
                    pageToken=response['nextPageToken']
                ).execute()
            else:
                break

