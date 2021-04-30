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

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey="AIzaSyAViOEVGzy-FigDtvCw3rvfOu678wOUq7I")

q= "samsung pop"
search_response = youtube.search().list(
    q=q,
    order="relevance",
    part="id,snippet",
    maxResults=10,
    type="channel"
    ).execute()

videos = []
channels = []
playlists = []
# Add each result to the appropriate list, and then display the lists of
# matching videos, channels, and playlists.

for idx,search_result in enumerate(search_response.get("items")):

    if search_result["snippet"]["title"].lower() == q:
        channel_id = search_result["id"]["channelId"]
        title = unescape(search_result["snippet"]["title"])
        channels.append(channel_id)


channel_id= channels[0]

# search_response = youtube.search().list(
#                     channelId=channel_id,
#                     order="viewCount",
#                     part="id,snippet",
#                     maxResults=50,
#                     type='video',
#                     ).execute()

# while search_response:
#     itemse = search_response['items']
#     if 'nextPageToken' in search_response:
#         itemse = itemse.extend(
#             youtube.search().list(
#                         channelId=channel_id,
#                         order="viewCount",
#                         part="id,snippet",
#                         maxResults=50,
#                         type='video',
#                         pageToken=search_response['nextPageToken']
#                         ).execute())
#
#     else:
#         print(itemse)
#         print('all contents is crawled')
#         break

    # elif search_result["id"]["kind"] == "youtube#channel":
    #     channels.append("%s (%s)" % (search_result["snippet"]["title"],
    #                                  search_result["id"]["channelId"]))
    # elif search_result["id"]["kind"] == "youtube#playlist":
    #     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
    #                                   search_result["id"]["playlistId"]))

# print("Videos:\n", "\n".join(videos), "\n")
# print("Channels:\n", "\n".join(channels), "\n")
# print("Playlists:\n", "\n".join(playlists), "\n")