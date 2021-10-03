from django.contrib.auth import get_user_model
from rest_framework import serializers

from newsfeed_portal.newsfeed.models import Country, News, Source

User = get_user_model()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "code", "name"]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "code", "name"]


class NewsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    source = SourceSerializer()

    class Meta:
        model = News
        fields = ["headline", "thumbnail", "url", "country", "source"]
