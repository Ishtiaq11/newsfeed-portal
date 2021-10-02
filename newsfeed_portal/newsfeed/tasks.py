from celery.utils.log import get_task_logger

from config import celery_app
from newsfeed_portal.newsfeed.models import News
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings
from newsfeed_portal.newsfeed.utils import build_payload, get_top_headlines

logger = get_task_logger(__name__)


@celery_app.task()
def scrape_top_headlines():
    """Scrape top headlines for countries and sources those are referred by user"""
    country_codes = (
        NewsFeedSettings.countries.through.objects.prefetch_related("country")
        .values_list("country__code", flat=True)
        .distinct()
    )
    for country_code in country_codes:
        save_news_in_db.apply_async(kwargs={"country": country_code})

    sources = (
        NewsFeedSettings.sources.through.objects.prefetch_related("source")
        .values_list("source__code", flat=True)
        .distinct()
    )
    # can query multiple sources in a reqeust
    sources_str = ",".join(sources)
    save_news_in_db.apply_async(kwargs={"sources": sources_str})


@celery_app.task()
def save_news_in_db(**kwargs):
    logger.info(f"Invoked `save_news_in_db` with params: #{kwargs}")
    try:
        news_list = get_top_headlines(**kwargs)
        logger.info(f"Got {len(news_list)} news from api")
        count = 0
        for news_data in news_list:
            try:
                # logger.info(f"News data: {news_data}")
                payload = build_payload(data=news_data, **kwargs)
                obj = News.objects.filter(url=payload.get("url")).first()
                if not obj:
                    obj = News.objects.create(**payload)
                    logger.info(f"Successfully saved news #id - {obj.id}")
                    count += 1
                else:
                    logger.info(
                        f"News already exists in our database. URL: {payload['url']}"
                    )
            except Exception as ex:
                logger.info(f"Failed to save news. Execption: {ex}")
        logger.info(f" Successfully saved {count} news")
    except Exception as ex:
        logger.info(ex)
        return []
