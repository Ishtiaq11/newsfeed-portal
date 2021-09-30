from django import forms

from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = NewsFeedSettings
        exclude = [""]
        widgets = {
            "user": forms.HiddenInput(),
        }
