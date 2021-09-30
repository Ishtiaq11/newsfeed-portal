from django.urls import path

from newsfeed_portal.newsfeed.views import SettingsUpdateView

app_name = "newsfeed"
urlpatterns = [
    path("settings/", view=SettingsUpdateView.as_view(), name="settings"),
]
