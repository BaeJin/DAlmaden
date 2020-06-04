from almaden import Sql
import requests
from bs4 import BeautifulSoup
import re

CUSTOM_HEADER = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cookie': 'SID=re88s5q4vs9qh73taceuk321va; musicoin_CID=9aaa30b8790546b3bb2f4e2a7f5d765d; _fbp=fb.1.1591150903804.1617704120; _ga=GA1.2.1792468374.1591150904; _gid=GA1.2.304244668.1591150904; _gat_gtag_UA_101753043_1=1',
    'referer': 'https://www.musicow.com/song/',#+songnum
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}


def crawl_list() :
    db = Sql("khroma")
    page = 1
    while True :
        print("페이지 : ",page)

        url_list = "https://www.musicow.com/auctions?tab=closed&keyword=&page="+str(page)
        CUSTOM_HEADER['referer'] = url_list
        r1 = requests.get(url_list, headers=CUSTOM_HEADER)
        bs1 = BeautifulSoup(r1.text,'html.parser')
        song_list = bs1.select('ul.user_buy li')
        for song in song_list :
            url2_add = song.a["href"]
            songID = url2_add.split("/")[2].strip()
            print(songID)
            txt = song.select('div.txt dl')
            title = txt[0].dd.text
            singer = txt[1].dd.text
            auctionDate = txt[2].dd.text

            db.insert_withoutDuplication('musicow_list', check_list=['songID'],
                                         songID=songID,
                                         title=title,
                                         singer=singer,
                                         auctionDate=auctionDate)
            crawl_auction(songID)
        page += 1
        if len(song_list) == 0:
            break

def crawl_auction(songID) :
    try :
        print(songID)
        songID = str(songID)
        db = Sql("khroma")
        url = "https://www.musicow.com/auction/%s"%(songID)
        CUSTOM_HEADER['referer'] = url
        r = requests.get(url, headers=CUSTOM_HEADER)
        bs = BeautifulSoup(r.text, 'html.parser')

        text_info = bs.select_one('#tab1').script.text.split(";")
        profit_raw = re.sub("[A-z=\s]", "", text_info[2])
        profit_info = re.sub(".+'", "", profit_raw)
        print(profit_info)
        auction = bs.select('dl.price strong')
        auctionAmount = int(re.sub("\D", "", auction[1].text))
        auctionStartPrice = int(re.sub("\D", "", auction[2].text))
        #auctionLowPrice = int(re.sub("\D", "", auction[2].text))
        #auctionAvgPrice = int(re.sub("\D", "", auction[3].text))
        print(auctionStartPrice)
        info_list = bs.select('div.lst_bul p')
        share_raw = re.sub("\s", "", info_list[0].text)
        shares = int(share_raw.replace("1/", "").replace(",", ""))
        print(shares)
        db.insert_withoutDuplication('musicow_auction', check_list=['songID'],
                                     songID=songID,
                                     profit_info=profit_info,
                                     shares=shares,
                                     auctionAmount=auctionAmount,
                                     auctionStartPrice=auctionStartPrice
                                     )
    except Exception as ex :
        print(ex)


def crawl_deal() :
    db = Sql("khroma")
    page = 1
    num = 0
    while True :
        print("페이지 : ",page)

        url_deal = "https://www.musicow.com/auctions?tab=market&keyword=&sortorder=&page=%d"%(page)
        CUSTOM_HEADER['referer'] = url_deal
        r1 = requests.get(url_deal, headers=CUSTOM_HEADER)
        bs1 = BeautifulSoup(r1.text,'html.parser')

        song_list = bs1.select('#list li')
        for song in song_list :
            num+=1
            url2_add = song.a["href"]
            dealID = url2_add.split("/")[2].strip()
            print(dealID)
            txt = song.select('div.txt dl')
            title = txt[0].dd.text
            singer = txt[1].dd.text
            currentPrice = int(re.sub("\D","",txt[2].dd.text))

            update = db.insert('musicow_deal',
                             dealID=dealID,
                             title=title,
                             singer=singer,
                             currentPrice=currentPrice,
                             num_order=num)
        page += 1
        if len(song_list) == 0:
            break

def update_info() :
    db = Sql("khroma")
    dealID_data = db.select("musicow_deal","dealID")
    dealID_list = set([d["dealID"] for d in dealID_data])
    for dealID in dealID_list :
        try :
            print(dealID)
            url = "https://www.musicow.com/song/%s?tab=info"%(dealID)
            CUSTOM_HEADER['referer'] = url
            r = requests.get(url, headers=CUSTOM_HEADER)
            bs = BeautifulSoup(r.text, 'html.parser')
            title = bs.select_one('strong.song_title').text.strip()
            singer = bs.select_one('span.artist').text.strip()
            auction = bs.select('div.row-col-2 dd')
            auctionAmount = int(re.sub("\D", "", auction[0].text))
            auctionStartPrice = int(re.sub("\D", "", auction[1].text))
            auctionLowPrice = int(re.sub("\D", "", auction[2].text))
            auctionAvgPrice = int(re.sub("\D", "", auction[3].text))

            db.insert_withoutDuplication('musicow_info', check_list=['dealID'],
                                         dealID=dealID,
                                         title=title,
                                         singer=singer,
                                         auctionAmount1=auctionAmount,
                                         auctionStartPrice1=auctionStartPrice,
                                         auctionLowPrice1=auctionLowPrice,
                                         auctionAvgPrice1=auctionAvgPrice
                                         )
        except Exception as ex :
            print(ex)
