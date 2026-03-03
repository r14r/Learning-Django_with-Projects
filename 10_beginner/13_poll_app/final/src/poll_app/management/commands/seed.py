from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from poll_app.models import Choice, Poll

POLLS = [
    {
        'question': 'What is your favorite Python web framework?',
        'description': 'Choose your go-to framework for web development.',
        'choices': ['Django', 'Flask', 'FastAPI', 'Tornado'],
    },
    {
        'question': 'Which database do you prefer?',
        'description': 'Select the database you use most often.',
        'choices': ['PostgreSQL', 'MySQL', 'SQLite', 'MongoDB'],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample polls'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True},
        )
        if not user.has_usable_password():
            user.set_password('admin')
            user.save()

        for data in POLLS:
            poll, created = Poll.objects.get_or_create(
                question=data['question'],
                defaults={'description': data['description'], 'author': user},
            )
            if created:
                for text in data['choices']:
                    Choice.objects.create(poll=poll, text=text)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(POLLS)} polls.'))
