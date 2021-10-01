from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Source(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    countries = models.ManyToManyField(
        Country, blank=True, related_name="settings_list"
    )
    sources = models.ManyToManyField(Source, blank=True, related_name="settings_list")
    keywords = TaggableManager(
        verbose_name="Keywords",
        blank=True,
        help_text="A comma-separated list of keywords",
    )

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"{self.user}'s newsfeed settings"


class News(models.Model):
    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.CASCADE
    )
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.CASCADE)
    headline = models.TextField(blank=True, null=True)
    thumbnail = models.URLField(max_length=500)
    url = models.URLField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.headline}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
