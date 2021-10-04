from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from newsfeed_portal.newsfeed.api.views import (
    CountryViewSet,
    NewsFeedSettingsViewSet,
    NewsViewSet,
    SourceViewSet,
)
from newsfeed_portal.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("news", NewsViewSet)
router.register("sources", SourceViewSet)
router.register("countries", CountryViewSet)

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path(
        "settings/",
        NewsFeedSettingsViewSet.as_view({"get": "retrieve", "put": "update"}),
    ),
]
