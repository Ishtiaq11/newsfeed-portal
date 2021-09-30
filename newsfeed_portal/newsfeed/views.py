from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from newsfeed_portal.newsfeed.forms import SettingsForm
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings


class SettingsUpdateView(LoginRequiredMixin, View):
    template_name = "newsfeed/newsfeed_settings.html"
    form_class = SettingsForm
    initial = {}
    instance = None
    success_url = reverse_lazy("home")
    success_message = "Updated settings successfully"

    def get_object(self):
        obj = NewsFeedSettings.objects.filter(user=self.request.user).first()
        return obj

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            instance=self.get_object(), initial={"user": request.user}
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {"form": form})
