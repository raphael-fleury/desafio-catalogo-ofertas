from django.core.management.base import BaseCommand
from products.scraper import collect_data

class Command(BaseCommand):
    help = "Scrapes product data from Mercado Livre and stores it in the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting scraping...")
        collect_data()
        self.stdout.write(self.style.SUCCESS("Scraping done with success!"))