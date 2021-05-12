import requests


def send_request():
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/",
        params={
            "api_key": "XAZN5Y277PEU020TOQWCSZL8PXCM3AKBZPXTX67S6ZBO7Y7QXC9WTV0T7O2EK4QRWR0O2I3Z0F0EM92X",
            "url": "https://www.coupang.com/vp/product/reviews?productId=281480779&page=2&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true",
            "render_js": "false",
        },
    )
    return response
headers = {
    'authority': 'www.coupang.com',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'PCID=16185750214525097140297; MARKETID=16185750214525097140297; _fbp=fb.1.1618575024662.1694033847; sid=20f500cfe71342d2a25cfeb35eb62156819c413c; bm_sz=EF717191352A44539102D7CCC05D02E5~YAAQrOQ1FzQiOUB5AQAAx2UWXwtfgWsF2YQz4nNE6tDn5YMTBdzaIdnB18FAiQG7gDWdHnNJGykH7CGBvh+1JXAWdUACfSrUl1eQ6Ke+sKHbDySGb4yXI73rSPK6taItvPGp1t6m8wIY9fHTCpDRz4yC4rTKRr+azPUBe1YdL5MiTGB7YXBfNL8xGA1M7a497w==; _abck=8C5E3E15CF127A868DB63C11BD57ABCE~0~YAAQrOQ1FzUiOUB5AQAAx2UWXwU7twWMZ0hH9OWjSLFyV5p2RrnPESs8G5KWqOKVLyqMUDGLjadANybnhpiW31cB0OKhPRnKwTMbORLZiXXXtBTDL10/++X2Tn1jbmlMYa2l/o7w+ERJsgxCLw0WKdxyNLYA8UqI8YFXQVwLmQxQsBTx0HYS1FTBvQtay19zb8rEoEiPJL+0Xhjt8C+r+ctV9Td6Ugl2os7rta958Nm34gNSS9YJhgzhwyTU6d4AdpKfu+X7j5Kl+NDfzL1nbsix9+CWXdzKRJcqwYOgMjnxjHJ24vvCiTX36NFCIRIzup+W1dw4rAxHR7UM5spUhA3qbnykvYHytXJnBpjeXlZ7nxOMXFOzta8f3VSP2Sr0rYJ3itBaEZUYgOnT9uQbzWQBA2fhENVlGw==~-1~-1~-1; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=^%^EC^%^BF^%^A0^%^ED^%^8C^%^A1; trac_itime=20210512143934; bm_mi=84D6CE862BDA04305F302D94FC91B2FD~GHQhWAU966zsNJVtY9yuOjBUGa7g66EAMdToxIbndhA1gDClDQMkAgTG4tgUWzPARf6wcUukkqHXfXN7VNhsmSP1zIuftUeWH1H3u8D9Hc0JoSSiy98heknPEpgWM7Cl3U8kqT3Mb8iHOYxeRbr6C4jvp9csASaUFgWWkDavicYrajrwLwm8O9q+T49fLpLA/iNcRwyxup3TA4Fwq4PC/fNqUMN6+/XqhEABTTLYWiUXKIpjqi9//lyWgE5XIRUxMqWWbr2wthuVvIulHBoT6w==; ak_bmsc=EC842797524D0E4001AEA8F1DA4F1E6E1735E4AC4A7C0000156A9B60E0FA857E~pl/5E/xLB+NFrfLF71DOOiJMeD+8RKGiKNLW+uWy3akYaOOd/meDg1zHBeV3I9wkRvDFd7rPi7n/2Vy/dHVSfLiO0yt1lRZgxmzjF87a2QM9Kg6mXb3ZsOb7jlkZLSnPZk6clo1iOu4iLRMgj/ktGyfbaRMd4FJWOZwNKSR5bWKoFPgCuZ82vJXuiZsKEYcoms/vuSy5kp5glCnmHeZkoNfyCCnFdZ4M438+kiiGZJUWjhL9L9ICxi/AGbLV40SmFT; overrideAbTestGroup=^%^5B^%^5D; baby-isWide=small; bm_sv=07EF0601685977932AE077281D8C5792~ZBxFqYDqqi0ysT2NBKwVOHATLyC33pSjeHapFrZEx1pkY+kCRdqij6p1yLGksyWod361q93+awni4j5jMk5ExrtwnbVfhq+SdiAHMScdegpvFoR97Ur01SE46P4UwDWTO+v8FvzSuDMX/THfg8Rb5i85o7P7qklHnt7UZgSuL3w=',
}


# data = {
#     "productId":281480779,
#     "page":1,
#     "size":5,
#     "sortBy":"ORDER_SCORE_ASC",
#     "ratings":"",
#     "q":"",
#     "viRoleCode":3,
#     "ratingSummary":"true"
#         }

response = send_request()
print(response.text)