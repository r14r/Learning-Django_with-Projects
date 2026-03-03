from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from url_shortener.models import ShortURL

URLS = [
    {'original_url': 'https://www.djangoproject.com', 'short_code': 'django1'},
    {'original_url': 'https://docs.python.org/3/', 'short_code': 'pydocs'},
    {'original_url': 'https://github.com', 'short_code': 'ghub01'},
]


class Command(BaseCommand):
    help = 'Seed the database with sample shortened URLs'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True},
        )
        if not user.has_usable_password():
            user.set_password('admin')
            user.save()

        for data in URLS:
            ShortURL.objects.get_or_create(
                short_code=data['short_code'],
                defaults={
                    'original_url': data['original_url'],
                    'created_by': user,
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(URLS)} short URLs.'))
