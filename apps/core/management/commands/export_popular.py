from django.core.management.base import BaseCommand
from scripts.export_popular_data import export_popular_data


class Command(BaseCommand):
    help = "Export 1000 most popular authors and related data"

    def handle(self, *args, **options):
        self.stdout.write("Starting export...")
        export_popular_data()
        self.stdout.write(self.style.SUCCESS("Export completed"))
