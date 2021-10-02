import json
import logging

from django.conf import settings
from newsapi import NewsApiClient

from config.settings.base import env
from newsfeed_portal.newsfeed.models import Country, Source

logger = logging.getLogger(__name__)


def get_top_headlines(*args, **kwargs):
    try:
        newsapi = NewsApiClient(api_key=env("NEWS_API_KEY"))

        response = newsapi.get_top_headlines(**kwargs)
        if response.get("status") == "ok":
            return response["articles"]
    except Exception as ex:
        logger.info("get_top_headlines error", ex)
        return []


def get_countries_map():
    file_path = settings.APPS_DIR / "static/data/countries.json"
    with open(file_path, "r") as f:
        return json.load(f)


def build_payload(data=dict(), **kwargs):
    """Build payload from news api data to create News object. This function is used by `save_news_in_db` task."""
    try:
        payload = dict()
        country = None
        if "country" in kwargs:
            country = Country.objects.get(code=kwargs["country"])
        if "source" not in data:
            raise ValueError("No source found for this news")
        source = None
        if data["source"].get("id"):
            source = Source.objects.get(code=data["source"]["id"])
        payload.update(
            country=country,
            source=source,
            headline=data.get("title"),
            thumbnail=data.get("urlToImage"),
            url=data.get("url"),
            description=data.get("descripttion"),
            published_at=data.get("publishedAt"),
        )

        return payload
    except Country.DoesNotExist as ex:
        logger.info(f"Country Does not Exist, country: {kwargs['country']}")
        raise ex
    except Source.DoesNotExist as ex:
        logger.info(f"Source Does not Exist, source: {data['source']['id']}")
        raise ex
    except Exception as ex:
        logger.info(
            f"Failed to build payload. Exception: {ex}, source: {data['source']['id']}"
        )
        raise ex
