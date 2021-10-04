from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from newsfeed_portal.newsfeed.models import Country, News
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings
from newsfeed_portal.newsfeed.models import Source

User = get_user_model()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["code", "name"]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["code", "name"]


class NewsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    source = SourceSerializer()

    class Meta:
        model = News
        fields = ["headline", "thumbnail", "url", "country", "source"]


class NewsFeedSettingsSerializer(TaggitSerializer, serializers.ModelSerializer):
    countries = CountrySerializer(many=True)
    sources = SourceSerializer(many=True)
    keywords = TagListSerializerField()

    class Meta:
        model = NewsFeedSettings
        fields = ["user", "sources", "countries", "keywords"]
