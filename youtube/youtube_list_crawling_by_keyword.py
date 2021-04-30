from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from youtube.source.account import accounts
from bs4 import BeautifulSoup
from html import unescape
import re as _re
import json

def convert_named_character(text):
    _charref = _re.compile(r'&(#[0-9]+;?'
                           r'|#[xX][0-9a-fA-F]+;?'
                           r'|[^\t\n\f <&#;]{1,32};?)')


    text = _charref.sub('',text)
    return text

DEVELOPER_KEY = accounts.get_api_key()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey="AIzaSyBM_BU6NjFb8cjr_doUB2UcnYY-b7S839o")

search_response = youtube.search().list(
    q="세븐나이츠",
    order="viewCount",
    part="id,snippet",
    maxResults=50,
    type="video"
    ).execute()

videos = []
channels = []
playlists = []
print(search_response)

# Add each result to the appropriate list, and then display the lists of
# matching videos, channels, and playlists.


for idx,search_result in enumerate(search_response.get("items")):

    if search_result["id"]["kind"] == "youtube#video":
        video_id = search_result["id"]["videoId"]

        title = unescape(search_result["snippet"]["title"])
        post_date = search_result["snippet"]["publishedAt"].split("T")[0]
        description = unescape(search_result["snippet"]["description"])
        thumbnails = search_result["snippet"]["thumbnails"]["default"]["url"]
        text_memo = json.dumps(search_result,ensure_ascii=False)

        print(text_memo)

    # elif search_result["id"]["kind"] == "youtube#channel":
    #     channels.append("%s (%s)" % (search_result["snippet"]["title"],
    #                                  search_result["id"]["channelId"]))
    # elif search_result["id"]["kind"] == "youtube#playlist":
    #     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
    #                                   search_result["id"]["playlistId"]))

# print("Videos:\n", "\n".join(videos), "\n")
# print("Channels:\n", "\n".join(channels), "\n")
# print("Playlists:\n", "\n".join(playlists), "\n")