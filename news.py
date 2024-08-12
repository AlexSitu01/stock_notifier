import requests
import os
from dotenv import load_dotenv
load_dotenv()
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_TOKEN = os.environ.get("NEWS_TOKEN")
class News:
    @staticmethod
    def get_news(keyword: str) -> str:
        news_params = {
            "q": keyword,
            'apiKey': NEWS_TOKEN
        }
        response = requests.get(url=NEWS_ENDPOINT, params=news_params)
        data = response.json()
        article = data["articles"][0]
        title = article["title"]
        description = article["description"]
        source = article["source"]["name"]
        url = article["url"]
        output = source + "\n" + title + "\n" + description + "\n" + url + "\n"
        return output
