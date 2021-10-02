from django.urls import path

from newsfeed_portal.newsfeed.views import NewsFeedHome, SettingsUpdateView

app_name = "newsfeed"
urlpatterns = [
    path("", view=NewsFeedHome.as_view(), name="home"),
    path("settings/", view=SettingsUpdateView.as_view(), name="settings"),
]
