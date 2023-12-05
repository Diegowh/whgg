from django.core.management.base import BaseCommand
from summoner_profile.updates.updater import Updater

class Command(BaseCommand):
    help = "Updates the database with the latest items and summoner spells"
    
    def handle(self, *args, **options):
        updater = Updater()
        updater.force_update()
        
        self.stdout.write(self.style.SUCCESS('Database updated successfully'))