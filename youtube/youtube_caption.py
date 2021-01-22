#download the package by:  pip install pytube
from pytube import YouTube
import urllib.request
import re
from engine.sql.almaden import Sql
from datetime import datetime
from youtubesearchpython import SearchVideos
import json


db = Sql("datacast2")

def get_youtube_url_by_keyword(search_keyword):
    task_id = db.select('crawl_task', 'task_id', f'keyword=\"{search_keyword}\"')[0]['task_id']
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword.replace(" ",""))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    print(f'task_id:{task_id},search_keyword:{search_keyword},len(video_ids)')


    for idx,video_id in enumerate(video_ids):
        url = ''
        caption_code = ''
        caption_text = ''

        try:
            url = "https://www.youtube.com/watch?v=" + video_id
            source = YouTube(url)
            post_time = source.publish_date
            post_date = post_time.date()
            title = source.title
            caption_language_infos = source.captions.all()
            for caption_language_info in caption_language_infos:
                if 'en' in caption_language_info.code:
                    caption_code = caption_language_info.code
            en_caption = source.captions.get_by_language_code(caption_code)
            en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            captions = en_caption_convert_to_srt.splitlines()

            for idx, caption_info in enumerate(captions):
                print(caption_info)
                if idx % 4 == 2:
                    caption_text += caption_info
            db.insert_withoutDuplication('crawl_contents',
                                         ['task_id','url'],
                                          task_id=task_id,
                                          url=url,
                                          post_time=post_time,
                                          post_date=post_date,
                                          title=title,
                                          text=caption_text)
        except Exception as e:
            print(url, caption_code, idx, video_id, e)

search_keyword = 'tesla power wall'
get_youtube_url_by_keyword(search_keyword)
