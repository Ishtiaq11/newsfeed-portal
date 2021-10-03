from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from newsfeed_portal.newsfeed.api.views import NewsViewSet
from newsfeed_portal.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("news", NewsViewSet)


app_name = "api"
urlpatterns = router.urls
