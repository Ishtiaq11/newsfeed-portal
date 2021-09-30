from django.contrib import admin

from newsfeed_portal.newsfeed.models import Country, Keyword
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


class KeywordAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


admin.site.register(Keyword, KeywordAdmin)


class NewsFeedSettingsAdmin(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(NewsFeedSettings, NewsFeedSettingsAdmin)
