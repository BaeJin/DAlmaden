import requests

cookies = {
    '5bb1fb4dd3c1ac0477ba0f972aa2c816': '1620795838700',
    'JSESSIONID': 'jxEhBT81WmEa11oSp4iQf0n6UNmLsjqw0PZJaQyqz8gPlDTDJ73PMunYus5lIQNZ.cE95bWFsbF9kb21haW4vb3ltcHByZDMx',
    'WMONID': 'zVzIzzpkpsX',
    'wl_chlNo': '6',
    'wl_chlDtlNo': '11',
    'RB_PCID': '1620795756310167228',
    'sch_check': 'yes',
    '_gcl_aw': 'GCL.1620795758.CjwKCAjw1uiEBhBzEiwAO9B_HXIL0Dq1j00G_MG8jX7tTtezfdDeA2p0qkJ59bunGYfM4qK75-WRThoC4bYQAvD_BwE',
    '_gcl_au': '1.1.96881331.1620795758',
    'PCID': '16207957576834193872470',
    '_gid': 'GA1.3.567695150.1620795758',
    '_gac_UA-181867310-1': '1.1620795758.CjwKCAjw1uiEBhBzEiwAO9B_HXIL0Dq1j00G_MG8jX7tTtezfdDeA2p0qkJ59bunGYfM4qK75-WRThoC4bYQAvD_BwE',
    '_gac_UA-92021806-1': '1.1620795758.CjwKCAjw1uiEBhBzEiwAO9B_HXIL0Dq1j00G_MG8jX7tTtezfdDeA2p0qkJ59bunGYfM4qK75-WRThoC4bYQAvD_BwE',
    '_trs_id': 'eY27472%3E724517%3F10',
    '_trs_sid': 'G%5B646541565046%5Bg%5B05650%3C506735%3D32',
    '_trs_flow': '',
    'EG_GUID': 'd9cb6a60-e38f-47db-8b98-9c8aff2429a8',
    'oliveyoung_CID': '253d2d0754d14143982f6df1c03572bd',
    '_fbp': 'fb.2.1620795758732.1127139566',
    '_gac_UA-92021806-9': '1.1620795759.CjwKCAjw1uiEBhBzEiwAO9B_HXIL0Dq1j00G_MG8jX7tTtezfdDeA2p0qkJ59bunGYfM4qK75-WRThoC4bYQAvD_BwE',
    'productHistory': '[{"goodsNo":"A000000120543","viewCount":3}]',
    '_ga_GMKKBJ29S2': 'GS1.1.1620795757.1.1.1620795839.59',
    'wcs_bt': 's_3ee47970f314:1620795839',
    '_gat_UA-92021806-9': '1',
    '_ga': 'GA1.3.673411431.1620795758',
    '_gat_UA-181867310-1': '1',
    '_gat': '1',
    'RB_SSID': 'chURWlBOzN',
    '_ga_9DTE0B1S0L': 'GS1.1.1620795757.1.1.1620795843.0',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000120543&trackingCd=Scp',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

params = (
    ('goodsNo', 'A000000120543'),
    ('gdasSort', '05'),
    ('itemNo', 'all_search'),
    ('pageIdx', '2'),
    ('colData', ''),
    ('keywordGdasSeqs', ''),
    ('type', ''),
    ('point', ''),
    ('hashTag', ''),
    ('optionValue', ''),
    ('cTypeLength', '0'),
)

response = requests.get('https://www.oliveyoung.co.kr/store/goods/getGdasNewListJson.do', headers=headers, params=params, cookies=cookies)
data = response.json()
reviews = data["gdasList"]
for review in reviews:
    print(review['gdasCont'])
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.oliveyoung.co.kr/store/goods/getGdasNewListJson.do?goodsNo=A000000120543&gdasSort=05&itemNo=all_search&pageIdx=2&colData=&keywordGdasSeqs=&type=&point=&hashTag=&optionValue=&cTypeLength=0', headers=headers, cookies=cookies)
