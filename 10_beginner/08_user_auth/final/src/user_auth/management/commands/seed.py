from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed the database with demo users'

    def handle(self, *args, **kwargs):
        users = [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'password': 'alice1234!',
                'profile': {'bio': 'Hi, I am Alice!', 'location': 'New York'},
            },
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password': 'bob12345!',
                'profile': {'bio': 'Bob here.', 'location': 'San Francisco', 'website': 'https://example.com'},
            },
        ]
        for data in users:
            profile_data = data.pop('profile')
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(**data)
                for k, v in profile_data.items():
                    setattr(user.profile, k, v)
                user.profile.save()
        self.stdout.write(self.style.SUCCESS('Seeded 2 demo users (alice, bob).'))
