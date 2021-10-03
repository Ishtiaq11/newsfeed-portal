import traceback

from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404

from config import celery_app
from newsfeed_portal.newsfeed.models import News
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings
from newsfeed_portal.newsfeed.utils import build_payload, get_top_headlines

logger = get_task_logger(__name__)

User = get_user_model()


@celery_app.task(name="Scrape news")
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


@celery_app.task(name="Save news")
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
                    find_users_by_keywords_for_email_notification.apply_async(
                        kwargs={"news_id": obj.id}
                    )
                else:
                    logger.info(
                        f"News already exists in our database. URL: {payload['url']}"
                    )
            except Exception as ex:
                logger.info(f"Failed to save news. Execption: {ex}")
        logger.info(f" Successfully saved {count} news")
        return count
    except Exception as ex:
        logger.info(ex)


@celery_app.task(name="Find users")
def find_users_by_keywords_for_email_notification(news_id):
    """Find users who will see this news. Then check"""
    try:
        news = get_object_or_404(News, id=news_id)
        # find users those will see the news in their newsfeed
        qs = (
            NewsFeedSettings.objects.filter(
                Q(countries__in=[news.country])
                | Q(sources__in=[news.source])
                | Q(Q(countries__isnull=True) & Q(sources__isnull=True))
            )
            .filter(keywords__isnull=False)
            .values_list("user__email", "keywords__name")
        )
        result = []
        for email, keyword in qs:
            if (news.headline and keyword in news.headline) or (
                news.description and keyword in news.description
            ):
                result.append((f"email={email} - keyword={keyword}, - news={news.id}"))
                send_email_notification.apply_async(
                    kwargs={"email": email, "news_id": news.id, "keyword": keyword}
                )
        return result
    except Exception:
        logger.info(f"Error: {traceback.format_exc()}")


@celery_app.task(name="Send Email")
def send_email_notification(email=None, news_id=None, keyword=None):
    logger.info(f"Start sending email to {email}")
    news = get_object_or_404(News, id=news_id)
    if email:
        result = send_mail(
            subject=f"{settings.EMAIL_SUBJECT_PREFIX} Got your preferred news containing {keyword}",
            message=f"{news.headline}-{news.url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        if result == 1:
            logger.info(f"Email sent to {email} successfully")
            return True
        else:
            logger.info(f"Failed to send email {email}")
            return False
