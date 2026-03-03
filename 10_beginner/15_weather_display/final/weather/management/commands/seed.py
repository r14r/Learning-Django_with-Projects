from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from weather.models import WeatherSearch

SEARCHES = [
    {'city': 'London', 'temperature': 15.0, 'condition': 'Partly cloudy', 'humidity': 72},
    {'city': 'Tokyo', 'temperature': 22.5, 'condition': 'Sunny', 'humidity': 55},
    {'city': 'New York', 'temperature': 18.0, 'condition': 'Clear', 'humidity': 60},
]


class Command(BaseCommand):
    help = 'Seed the database with sample weather searches'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True},
        )
        if not user.has_usable_password():
            user.set_password('admin')
            user.save()

        for data in SEARCHES:
            WeatherSearch.objects.create(user=user, **data)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(SEARCHES)} weather searches.'))
