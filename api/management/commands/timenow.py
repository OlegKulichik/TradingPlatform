from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):

    def handle(self, *args, **options):
        time = timezone.now().strftime("%H:%M:%S")
        self.stdout.write(f'Time is now {time}')
