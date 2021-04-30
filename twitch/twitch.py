import requests

headers = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': 'm5wusivcdu35b3cff2haxeo3gbtf69',
}

response = requests.get('https://api.twitch.tv/kraken/chat/44322889/badges', headers=headers)
print(response.text)