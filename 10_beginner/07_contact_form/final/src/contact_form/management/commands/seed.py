from django.core.management.base import BaseCommand
from contact_form.models import ContactMessage


class Command(BaseCommand):
    help = 'Seed the database with sample contact messages'

    def handle(self, *args, **kwargs):
        samples = [
            {
                'name': 'Alice Smith',
                'email': 'alice@example.com',
                'subject': 'Project Inquiry',
                'message': 'Hello, I would like to discuss a potential project.',
            },
            {
                'name': 'Bob Jones',
                'email': 'bob@example.com',
                'subject': 'Support Request',
                'message': 'I am having trouble with my account.',
                'is_read': True,
            },
            {
                'name': 'Carol White',
                'email': 'carol@example.com',
                'subject': 'Feedback',
                'message': 'Great service! Just wanted to share some feedback.',
            },
        ]
        for data in samples:
            ContactMessage.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(samples)} contact messages.'))
