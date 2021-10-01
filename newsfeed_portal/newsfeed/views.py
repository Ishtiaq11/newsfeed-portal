from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from newsfeed_portal.newsfeed.forms import SettingsForm
from newsfeed_portal.newsfeed.models import News
from newsfeed_portal.newsfeed.models import Settings as NewsFeedSettings


class SettingsUpdateView(LoginRequiredMixin, View):
    template_name = "newsfeed/newsfeed_settings.html"
    form_class = SettingsForm
    initial = {}
    instance = None
    success_url = reverse_lazy("newsfeed:home")
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
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class NewsFeedHome(ListView):
    model = News
    paginate_by = 4
    template_name = "newsfeed/home.html"

    def get_queryset(self):
        settings = (
            NewsFeedSettings.objects.filter(user=self.request.user)
            .prefetch_related("countries", "sources")
            .first()
        )
        news_list = News.objects.all().order_by("-published_at")
        if settings.countries.exists():
            news_list = news_list.filter(country__in=settings.countries.all())
        if settings.sources.exists():
            news_list = news_list.filter(source__in=settings.sources.all())
        return news_list
