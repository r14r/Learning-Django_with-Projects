from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from todo_list.models import Todo


class Command(BaseCommand):
    help = 'Seed database with default todos'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        user.set_password('admin123')
        user.save()

        todos = [
            ('Set up development environment', 'Install Python, Django, and VS Code', 'high', False),
            ('Read Django documentation', 'Focus on models, views, and templates chapters', 'high', False),
            ('Build first Django project', 'Follow the official tutorial', 'medium', True),
            ('Learn about Django ORM', 'Practice queries, filters, and relationships', 'medium', False),
            ('Deploy to production', 'Use Heroku or DigitalOcean for hosting', 'low', False),
        ]
        for title, desc, priority, done in todos:
            Todo.objects.get_or_create(
                title=title,
                defaults={'description': desc, 'priority': priority, 'is_done': done, 'author': user}
            )

        self.stdout.write(self.style.SUCCESS('Seeding complete: 5 todos created'))
