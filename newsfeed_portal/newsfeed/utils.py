import json
import traceback

from django.conf import settings
from newsapi import NewsApiClient

from config.settings.base import env
from newsfeed_portal.newsfeed.models import Country, News, Source


def get_top_headlines(*args, **kwargs):
    try:
        newsapi = NewsApiClient(api_key=env("NEWS_API_KEY"))

        response = newsapi.get_top_headlines(**kwargs)
        if response.get("status") == "ok":
            return response["articles"]
    except Exception as ex:
        print(ex)
        return []


def save_news(**kwargs):
    """Utility function to load news in database"""
    try:
        news_list = get_top_headlines(**kwargs)
        print(f"got {len(news_list)} news")
        country = None
        if kwargs.get("country"):
            country, created = Country.objects.get_or_create(code=kwargs.get("country"))
            if created:
                print(f"created country object. code #{country.code}")
        for news in news_list:
            print(f"news: {news}")
            news_obj = News()
            news_obj.country = country
            # news source
            news_source = news["source"]
            source_obj = None
            if news_source["id"] is not None:
                source_obj, created = Source.objects.get_or_create(
                    code=news_source["id"], name=news_source["name"]
                )
                if created:
                    print(
                        f"created source object. code #{source_obj.code}, name #{source_obj.name}"
                    )
            news_obj.source = source_obj
            news_obj.headline = news["title"]
            news_obj.url = news["url"]
            news_obj.thumbnail = news["urlToImage"]
            news_obj.description = news["description"]
            news_obj.published_at = news["publishedAt"]
            news_obj.save()
            print(f"Successfully created news. id: #{news_obj.id}")
    except Exception:
        track = traceback.format_exc()
        print(track)


def get_countries_map():
    file_path = settings.APPS_DIR / "static/data/countries.json"
    with open(file_path, "r") as f:
        return json.load(f)
