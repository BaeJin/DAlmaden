import requests

def get_reviews(appid, params):
        url = 'https://store.steampowered.com/appreviews/'
        response = requests.get(url=f"{url}/{appid}", params=params, headers={'User-Agent': 'Mozilla/5.0'})
        return response.json()

params = {'json':1}
response = get_reviews(289070, params)
print(response)