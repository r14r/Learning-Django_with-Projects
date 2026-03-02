from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from personal_portfolio.models import Project


class Command(BaseCommand):
    help = 'Seed database with portfolio projects'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        user.set_password('admin123')
        user.save()

        projects = [
            ('Django Blog Platform', 'A full-featured blog platform built with Django, supporting markdown, tags, and comments.', 'Python/Django', 'https://example.com', 'https://github.com'),
            ('React Dashboard', 'An analytics dashboard built with React and Chart.js, consuming a REST API backend.', 'React/JavaScript', '', 'https://github.com'),
            ('Mobile Weather App', 'A cross-platform mobile app built with Flutter showing real-time weather data.', 'Flutter/Dart', 'https://example.com', ''),
        ]
        for title, desc, tech, live, github in projects:
            Project.objects.get_or_create(
                title=title,
                defaults={'description': desc, 'technology': tech, 'live_url': live, 'github_url': github, 'author': user}
            )

        self.stdout.write(self.style.SUCCESS('Seeding complete: 3 portfolio projects created'))
