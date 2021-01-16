import requests
import json
import numpy as np

cookies = {
    'NRTK': 'ag#all_gr#1_ma#-2_si#0_en#0_sp#0',
    'NNB': 'GFWKWAX5XD2V6',
    'page_uid': 'U/TG/wp0JXossapGcNlssssstKK-151463',
    'nx_ssl': '2',
}

headers = {
    'authority': 'ssl.pstatic.net',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'script',
    'referer': 'https://search.shopping.naver.com/search/all?frm=NVSHTTL&origQuery=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&pagingIndex=1&pagingSize=40&productSet=total&query=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&sort=rel&timestamp=&viewType=list',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; _shopboxeventlog=false; NNB=GFWKWAX5XD2V6; page_uid=U/TG/wp0JXossapGcNlssssstKK-151463; nx_ssl=2; AD_SHP_BID=4; spage_uid=U%2FTG%2Fwp0JXossapGcNlssssstKK-151463',
    'Referer': 'https://search.shopping.naver.com/search/all?frm=NVSHTTL&origQuery=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&pagingIndex=1&pagingSize=40&productSet=total&query=%ED%97%A4%EC%96%B4%EB%93%9C%EB%9D%BC%EC%9D%B4%EA%B8%B0&sort=rel&timestamp=&viewType=list',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'if-none-match': '"3fa6-5b68dcea33640-gzip"',
    'if-modified-since': 'Wed, 16 Dec 2020 05:04:17 GMT',
    'urlprefix': '/api',
    'If-None-Match': '"rBZoLV4WqM2wAfbdh0VfwNSAj/8="',
    'Connection': 'keep-alive',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'image',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://search.shopping.naver.com',
    'pragma': 'no-cache',
    'Origin': 'https://search.shopping.naver.com',
}
sum_review = 0
for i in range(0,1):
    params = {'frm':'NVSHTTL',
              'pagingIndex':i,
              'pagingSize':'40',
              'productSet':'total',
              'catId':50001171,
              'sort':'rel',
              'viewType':'list'}

    response = requests.get('https://search.shopping.naver.com/search/category', headers=headers, params=params,cookies=cookies)
    data_to_json = json.loads(response.text)
    products_info = data_to_json['shoppingResult']['products']
    for idx, product_info in enumerate(products_info):
        _data = {}
        keys = product_info['attributeValue'].split("|")
        values = product_info['characterValue'].split("|")
        for idx2, key in enumerate(keys):
            if key not in _data.keys():
                _data[key] = values[idx2]
            else:
                _data[key] += ','+ values[idx2]
        for key in _data.keys():
            _data[key] = _data.get(key).split(",")

        json_data = json.dumps(_data,ensure_ascii=False)
        print(idx,json_data)

        reviewCount = product_info['reviewCount']
        #리뷰수, 용도, 중량, 가격, 부위, 리뷰수, 구매건수, 등록일’
        print(product_info['reviewCount'],  #리뷰수
              product_info['purchaseCnt'],  #구매건수
              product_info['openDate'],  #등록일
              product_info['characterValue'],  #용도 #부위 #중량
              product_info['price'],  #가격
              product_info['price'])
        sum_review += reviewCount

print(sum_review)
    # data_to_json = json.loads(response.text)
# data_to_json['']