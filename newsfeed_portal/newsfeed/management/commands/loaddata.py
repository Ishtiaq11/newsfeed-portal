import traceback

from django.core.management.base import BaseCommand, CommandError
from newsapi import NewsApiClient

from config.settings.base import env
from newsfeed_portal.newsfeed.models import Country, Source
from newsfeed_portal.newsfeed.utils import get_countries_map


class Command(BaseCommand):
    help = "Load country and source in database"

    def handle(self, *args, **options):
        try:
            newsapi = NewsApiClient(api_key=env("NEWS_API_KEY"))

            response = newsapi.get_sources()
            sources = []
            if response.get("status") == "ok":
                sources = response["sources"]
            country_map = get_countries_map()
            for source in sources:
                if source.get("id"):
                    source_obj, created = Source.objects.get_or_create(
                        code=source["id"]
                    )
                    if created:
                        source_obj.name = source.get("name")
                        source_obj.save()
                        # print(f"Created source #{source.id} - {source.name}")
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created source #{source_obj.code} - {source_obj.name}"
                            )
                        )
                if source.get("country"):
                    country_obj, created = Country.objects.get_or_create(
                        code=source["country"]
                    )
                    if created:
                        country_obj.name = country_map.get(source["country"].upper())
                        country_obj.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created country #{country_obj.code} - {country_obj.name}"
                            )
                        )

        except Exception as ex:
            track = traceback.format_exc()
            print(track)
            raise CommandError(ex)
