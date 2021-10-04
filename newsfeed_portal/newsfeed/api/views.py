import logging

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from newsfeed_portal.newsfeed.models import Country, News
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings
from newsfeed_portal.newsfeed.models import Source

from .serializers import (
    CountrySerializer,
    NewsFeedSettingsSerializer,
    NewsSerializer,
    SourceSerializer,
)

logger = logging.getLogger(__name__)


class NewsViewSet(ListModelMixin, GenericViewSet):
    queryset = News.objects.all().order_by("-published_at")
    serializer_class = NewsSerializer

    def get_queryset(self, *args, **kwargs):
        settings_obj = (
            NewsFeedSettings.objects.filter(user=self.request.user)
            .prefetch_related("countries", "sources")
            .first()
        )
        news_list = self.queryset
        if settings_obj.countries.exists():
            news_list = news_list.filter(country__in=settings_obj.countries.all())
        if settings_obj.sources.exists():
            news_list = news_list.filter(source__in=settings_obj.sources.all())
        logger.info(f"Total news in api {len(news_list)}")
        return news_list


class NewsFeedSettingsViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = NewsFeedSettingsSerializer
    queryset = NewsFeedSettings.objects.all()

    def get_object(self):
        return self.request.user.settings


class CountryViewSet(ListModelMixin, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class SourceViewSet(ListModelMixin, GenericViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
