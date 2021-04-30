import pickle
import csv
import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

DEVELOPER_KEY = "AIzaSyBM_BU6NjFb8cjr_doUB2UcnYY-b7S839o"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"
youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

comments, commentsId, repliesCount, likesCount, viewerRating = [], [], [], [], []

search_response = youtube.commentThreads().list(
    maxResults=100,
    order='time',
    videoId='BAD9EZFe0vs',
    part='snippet',
    textFormat='plainText'
    ).execute()
# print(search_response,len(search_response['items']))
for item in search_response['items']:
    # 5 index item for desired data features
    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    comment_id = item['snippet']['topLevelComment']['id']
    reply_count = item['snippet']['totalReplyCount']
    like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
    post_date = item['snippet']['topLevelComment']['snippet']['publishedAt'].split("T")[0]
    comments.append(comment)
    commentsId.append(comment_id)
    repliesCount.append(reply_count)
    likesCount.append(like_count)
    print(item)
# print(comments,commentsId,repliesCount,likesCount)
