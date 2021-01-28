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

comments = []

results = youtube.commentThreads().list(
    videoId = 'X7-aZpsnw5M',
    order='time',
    part = 'snippet',
    textFormat='plainText',
    maxResults = 100
    ).execute()

print(results)
