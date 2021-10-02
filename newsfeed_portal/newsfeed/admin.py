from django.contrib import admin

from newsfeed_portal.newsfeed.models import Country, News
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings
from newsfeed_portal.newsfeed.models import Source


class CountryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
    ]


admin.site.register(Country, CountryAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
    ]


admin.site.register(Source, SourceAdmin)


class NewsFeedSettingsAdmin(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(NewsFeedSettings, NewsFeedSettingsAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ["headline", "country", "source", "url"]
    list_per_page = 25
    list_filter = ["country", "source"]


admin.site.register(News, NewsAdmin)
