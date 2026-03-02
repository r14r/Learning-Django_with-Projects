from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from notes_app.models import Note

NOTES = [
    {'title': 'Welcome to Notes App', 'content': 'This is your first note. You can create, edit, and pin notes.', 'color': '#fff9c4'},
    {'title': 'Shopping List', 'content': 'Milk\nEggs\nBread\nButter\nCoffee', 'color': '#c8e6c9'},
    {'title': 'Project Ideas', 'content': 'Build a personal finance tracker\nLearn Rust\nContribute to open source', 'color': '#bbdefb'},
    {'title': 'Meeting Notes', 'content': 'Discussed Q4 roadmap\nAction items: review PR, update docs', 'color': '#f8bbd0', 'pinned': True},
    {'title': 'Recipes', 'content': 'Pasta: boil water, cook pasta, add sauce\nSalad: chop veggies, add dressing', 'color': '#e1bee7'},
]


class Command(BaseCommand):
    help = 'Seed the database with sample notes'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True},
        )
        if not user.has_usable_password():
            user.set_password('admin')
            user.save()

        for data in NOTES:
            Note.objects.get_or_create(
                title=data['title'],
                author=user,
                defaults={
                    'content': data['content'],
                    'color': data['color'],
                    'pinned': data.get('pinned', False),
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(NOTES)} notes.'))
