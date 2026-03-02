from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hello_django.models import Message


class Command(BaseCommand):
    help = 'Seed database with default messages'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        user.set_password('admin123')
        user.save()

        messages = [
            ('Welcome to Hello Django!', 'This is your first Django application. Explore the code to learn how it works.'),
            ('Django is awesome', 'Django makes it easy to build web applications with Python. Check out the documentation at djangoproject.com.'),
            ('Getting started', 'To get started, clone the repository, install dependencies, run migrations, and start the dev server.'),
        ]
        for title, body in messages:
            Message.objects.get_or_create(title=title, defaults={'body': body, 'author': user})

        self.stdout.write(self.style.SUCCESS('Seeding complete: 3 messages created'))
