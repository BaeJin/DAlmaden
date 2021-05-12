import requests

cookies = {
    'cguid': '11620797297773004371000000',
    'sguid': '31620797297773004371000000',
    'semagcd': '',
    'kwid': 'g0011595316651k4020093',
    'lnd_kwd': 'gp111',
    'PARTNERSHIP': 'PARTNERSHIP_HCODE=Y&PARTNERSHIP_BCODE=KD99999999&PARTNERSHIP_ID=867&PARTNERSHIP^%^5FHCODE=Y&PARTNERSHIP^%^5FBCODE=KD99999999&PARTNERSHIP^%^5FID=867',
    'PARTNERSHIP_ID': '867',
    'PARTNERSHIP_BCODE': 'KD99999999',
    'PARTNERSHIP^%^5FID': '867',
    'PARTNERSHIP^%^5FBCODE': 'KD99999999',
    'pcid': '1620797298535',
    'pguid': '21620797298636009861010000',
    'AGP': 'fccode=AJ47',
    'channelcode': 'AA12',
    'ASP.NET_SessionId': 'kddymzcjjln0vj1ckiuipefq',
    'WMONID': 'V9HvlH3ZfBw',
    'ssguid': '316207972986360098612900003',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://itempage3.auction.co.kr',
    'Referer': 'http://itempage3.auction.co.kr/detailview.aspx?ItemNo=B806985806&listqs=catetab^%^3d7^%^26selecteditemno^%^3dB806985806^%^26class^%^3dCorner.CategoryBest^%^26listorder^%^3d0&listtitle=^%^ba^%^a3^%^bd^%^ba^%^c6^%^ae100&frm2=through',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

# data = '^{^\\^itemNo^\\^:^\\^B806985806^\\^,^\\^filterParam^\\^:^\\^useruniqueid-11620797297773004371000000^\\^,^\\^sort^\\^:^\\^popular^\\^,^\\^pageIndex^\\^:2,^\\^totalCount^\\^:4530^}'
data_decode = {"itemNo":"B806985806", "filterParam":"useruniqueid-11620797297773004371000000","sort":"popular","pageIndex":2,"totalCount":4530}
response = requests.post('http://itempage3.auction.co.kr/WebService/ReviewService.asmx/GetReviewList', headers=headers, cookies=cookies, json=data_decode, verify=False)
response_data = response.json()['d']
print(response_data)