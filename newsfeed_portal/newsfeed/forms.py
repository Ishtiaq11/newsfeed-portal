from django import forms

from newsfeed_portal.newsfeed.models import News
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = NewsFeedSettings
        exclude = [""]
        widgets = {
            "user": forms.HiddenInput(),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = [""]
