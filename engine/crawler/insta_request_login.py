import requests

def instgram_login():
    LOGIN_INFO = {
        'username': 'jykim@almaden.co.kr',
        'password': 'almaden7025!',
        'queryParams': "{가방}"
    }
    InstagramSession = requests.session()
    getCSRF = InstagramSession.get("https://www.instagram.com/accounts/login")
    cookieString = str(getCSRF.cookies)
    LoginCSRFtoken = cookieString[37:69]
    print(cookieString)
    print(LoginCSRFtoken)
    RequestHeaders = {'origin': "www.instagram.com",
                      'method': 'POST',
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'x-requested-with': "XMLHttpRequest",
        'x-csrftoken': LoginCSRFtoken,
        'x-instagram-ajax': "de81cb3fd9c4-hot",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "*/*",
        'referer': "https://www.instagram.com/accounts/login/"
    }
    login = InstagramSession.post("https://www.instagram.com/accounts/login/ajax/", data=LOGIN_INFO, headers=RequestHeaders)
    print(login.status_code)
    return InstagramSession, RequestHeaders

instgram_login()