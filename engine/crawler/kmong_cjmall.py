import requests

cookies = {
    'SOT_UID': 'U6910fa2bf18a9e4408680e494e10e1e0f77f1620796898',
    'SOT_SID': 'U778d9f21e9533a4afdf8cf7a5063816562b61620796898',
    'SOT_FID': 'PoHCoXgNelM1CXbE9b11620796897531',
    'JSESSIONID_LIVELOG': '938C72F025089498B7E5F9BB6888293A',
    'RB_PCID': '1620796898730667526',
    '_ga': 'GA1.2.1015467360.1620796899',
    '_gid': 'GA1.2.1721432610.1620796899',
    'EG_GUID': '2f702a1f-595d-4b56-811e-2c6cac615772',
    '_gat_UA-170633634-3': '1',
    '_qg_fts': '1620796899',
    'QGUserId': '1812390370100199',
    '_qg_cm': '1',
    'UI_NHPrd': 'H4sIAAAAAAAAAPPV8TU0NDIzNjPWMTI0MDU0AgBeF0YAEQAAAA',
    'TS017ad49d': '01205c90cb77c730d8bab26dd2a6502e7445d5eb5a620bdeea71842a09e9846f9087bf1932add674943013c6a040bfe262203892259b2fe553ec3904fe75dccbc4fa2263a5b46b3d256f832af80ce63f8233609aa0eea416da7179c1850af0198141f8a75c',
    'SCOUTER': 'z6rgihsueen24a',
    'TS0170e56e': '01205c90cbabf710249df2b09045023da240ba6f3e907898b89d5be34ec292f17db422f1edd0ab34d9cf20671fdaf862f0a36fa65ed794ab7f0058e5083fd88615d7cfe08d',
    'RB_SSID': 'eUvULw3aU1',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '^\\^',
    'Accept': '*/*',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Origin': 'https://display.cjonstyle.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://display.cjonstyle.com/p/mocode/M1126363',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

params = (
    ('itemCode', '61564540'),
    ('mocode', ''),
    ('option1Cd', ''),
    ('option2Cd', ''),
    ('sortGbn', ''),
    ('imgAtchYn', ''),
    ('oneMonthYn', ''),
    ('reviewNo', ''),
    ('imgTag', ''),
    ('page', '1'),
)

response = requests.get('https://item.cjonstyle.com/celebshop/review/rest/itemReviewList', headers=headers, params=params, cookies=cookies)
reviews = response.json()
for review in reviews['result']:
    print(review['contents'])

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://item.cjonstyle.com/celebshop/review/rest/itemReviewList?itemCode=61564540&mocode=&option1Cd=&option2Cd=&sortGbn=&imgAtchYn=&oneMonthYn=&reviewNo=&imgTag=&page=1', headers=headers, cookies=cookies)
