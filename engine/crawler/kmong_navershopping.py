import requests

headers = {
    'authority': 'search.shopping.naver.com',
    'sec-ch-ua': '^\\^',
    'accept': 'application/json, text/plain, */*',
    'urlprefix': '/api',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://cr.shopping.naver.com/adcr.nhn?x=j12fA6ihnGNtkC0ZYyCGKv%2F%2F%2Fw%3D%3Ds%2BPsiHxQXuMpn4YuUSgrUOcmqEiq6OjrFN1rHlQHnch7zSOmTS42enKYm3kPOXLHl8WHA5RjWLfCN827qYWLHr1URgynFkMa1iEW7imT2D0TDpmNu2Rs3tEPrV0ZTODsb7JQtrMqSgEftbsAH7BzOjn7C8oLNURiEaE%2BZtoYBPlsi2D9FHsVFihtMV9WFYwR1gRokOxYiLF7s%2FPq4uTtLld9%2BKy%2Fm0d%2BgYWHtEf61Jo5CNclKwvLyA%2Fys%2F%2FHPPajLvZMdfslqBv6%2FzdsDQYyIaZK8LJLETsngefeCP0Z8nADPRx1i%2Bp%2Bk3hzlMJYFt6hqQxCjRgmCDthdtiT59JO9yovxjvDZ9umtgd6xeTqAA1hIAJ%2FJQ9vsa4G5awamMD3Visext5K2yYkF868rsMDqia%2BT6ZCOywRPfbjm%2FYdPAcwczY%2F8eCyfgopyQ9U22UU99UEMwi63jafLIzwwY0rYsbF%2Fh0Ht2fYRw5EqsonD2ydFUy6EAFE5jC7zg90uEgyjRYgXT8U0rr2Dm%2BuxQGAQBpSxfHDaV%2FO9PnQ2QqUCBx%2BYGVIpQWroqD6P8QiVmqU6sL8NsZuLrYcQe2suKiuA6WA2glWH1TKancJct29CHzqS9Of8p6VybKDDhGhaLORhRaWWQNozKbzfxBdqVYoTDXxSiGQZZq6WCPHj0EuB%2FU7ipqOSBSwGxwKjkzX1yddaB1jb8xDmz4mgtOb1rvGj1B6ZE%2BX0yPcxmdCnIlN0Vf4GruH08DlKshetxY8KUEZb&nvMid=26703328400&catId=50004666',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=RCAFITJ45R3GA; nx_ssl=2; AD_SHP_BID=24; pc_ranking_info=Y; NaverSuggestUse=unuse^%^26use; sus_val=h1lAk0woMFe7EVmMrppte8he; spage_uid=; ncpa=432352^|kol5wryw^|21f05720b79566d6ed5bdb6cbedddc1bb2b06caa^|s_28826208103388785^|f9eb24d2c2ce4413ee83818ab25a5c3d686f7324:1121368^|kol6511c^|a2489873a3bb09c469ebaec6819a7d2e1fddcf48^|s_2b4a1d3455e31^|5b51e0d0be1cc5c4532a083c16eb7ff37102986a:95694^|kol6544g^|f52b2dfd51115c2bc90d2084edd5aff78ac1fa4d^|null^|ae4ba32fac88e655ab563b02aaa3fdf74206f3b3',
}

params = (
    ('nvMid', '21911673202'),
    ('reviewType', 'ALL'),
    ('sort', 'QUALITY'),
    ('page', '1'),
)

response = requests.get('https://search.shopping.naver.com/review',headers=headers, params=params)
review_data_list = response.json()['reviews']
for idx,review in enumerate(review_data_list):
    print(idx,review)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://search.shopping.naver.com/review?nvMid=26123683678&reviewType=ALL&sort=QUALITY&isNeedAggregation=N&isApplyFilter=N&page=2&pageSize=20', headers=headers)
