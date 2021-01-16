#  Install the Python Requests library:
# `pip install requests`
import requests


def send_request():
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/",
        params={
            "api_key": "XAZN5Y277PEU020TOQWCSZL8PXCM3AKBZPXTX67S6ZBO7Y7QXC9WTV0T7O2EK4QRWR0O2I3Z0F0EM92X",
            "url": "https://www.instagram.com/explore/tags/3d%ED%94%84%EB%A6%B0%ED%84%B0/",
        },

    )
    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.content)


send_request()