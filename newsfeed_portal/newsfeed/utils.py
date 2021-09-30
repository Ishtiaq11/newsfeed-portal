from newsapi import NewsApiClient

from config.settings.base import env


def get_top_headlines(*args, **kwargs):
    try:
        newsapi = NewsApiClient(api_key=env("NEWS_API_KEY"))

        response = newsapi.get_top_headlines(**kwargs)
        if response.get("status") == "ok":
            return response["articles"]
    except Exception as ex:
        print(ex)
        return []
