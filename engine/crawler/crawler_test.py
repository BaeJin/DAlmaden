#  Install the Python Requests library:
# `pip install requests`
import requests


def send_request():
    return_url = '''
        url="https://app.scrapingbee.com/api/v1/",params={"api_key": "XAZN5Y277PEU020TOQWCSZL8PXCM3AKBZPXTX67S6ZBO7Y7QXC9WTV0T7O2EK4QRWR0O2I3Z0F0EM92X","url": "https://www.instagram.com/graphql/query/?query_hash=9b498c08113f1e09617a1703c22b2f32&variables=%7B%22tag_name%22%3A+%22%5Cub2e4%5Cub178%5Cuc2dd%5Cub2e8%22%2C+%22first%22%3A+20%2C+%22after%22%3A+%22QVFEV0NuZG5iWWtfSTBBcGdTMTJnQzVYYUZkOENjQkZncFgzczdsd01YdW84Q0hCVHBtRHQwZDhHVWo5alJ5S1o3dlNuX3g1c3h0cEZuM21XbzRwYzJLYg%3D%3D%22%7D","render_js": "false",},'''
    response = requests.get(return_url)

    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.text)


send_request()