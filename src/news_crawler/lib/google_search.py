from ..common.config import Config
import requests
from urllib.parse import quote

def search_from_google(query: str, start: int = 0):
    q = quote(query)
    key = quote(Config.google_api_key)
    cx = quote(Config.google_cx)
    date_restrict = 'w1'
    url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={q}&start={start}&dateRestrict={date_restrict}&sort=date"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Google Search API request failed with status code {response.status_code}")
        return []

    data = response.json()

    _list = []
    for item in data.get("items", []):
        _list.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })

    return _list
