from celery.task.sets import TaskSet
from newsapi import NewsApiClient

from config import celery_app
from config.settings.base import env
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings


@celery_app.task()
def scrape_top_headlines():
    """Scrape top headlines for countries and sources those are referred by user"""
    country_codes = (
        NewsFeedSettings.countries.through.objects.prefetch_related("country")
        .values_list("country__code", flat=True)
        .distinct()
    )
    subtasks = [
        get_top_headlines.subtask(kwargs={"country": country_code})
        for country_code in country_codes
    ]
    sources = (
        NewsFeedSettings.sources.through.objects.prefetch_related("source")
        .values_list("source__code", flat=True)
        .distinct()
    )
    # can query multiple sources in a reqeust
    sources_str = ",".join(sources)
    subtasks.append(get_top_headlines.subtask(kwargs={"sources": sources_str}))
    taskset = TaskSet(tasks=subtasks)
    taskset.apply_async()


@celery_app.task()
def get_top_headlines(**kwargs):
    try:
        newsapi = NewsApiClient(api_key=env("NEWS_API_KEY"))

        response = newsapi.get_top_headlines(**kwargs)
        if response.get("status") == "ok":
            return response["articles"]
    except Exception as ex:
        print(ex)
        return []
