from django.core.management.base import BaseCommand

from autobahn.services.autobahn_api_scrapping import sync_roadworks_with_api


class Command(BaseCommand):
    help = "Sync roadworks with API"

    def handle(self, *args, **options):
        sync_roadworks_with_api()
        self.stdout.write(self.style.SUCCESS("Sync comleted!"))
