from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Source(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Keyword(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    countries = models.ManyToManyField(
        Country, blank=True, null=True, related_name="settings_list"
    )
    sources = models.ManyToManyField(
        Source, blank=True, null=True, related_name="settings_list"
    )
    keywords = models.ManyToManyField(
        Keyword, blank=True, null=True, related_name="settings_list"
    )

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"{self.user}'s newsfeed settings"
