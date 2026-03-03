from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from web_calculator.models import Calculation


class Command(BaseCommand):
    help = 'Seed database with calculation history'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        user.set_password('admin123')
        user.save()

        calculations = [
            ('2 + 2', '4'),
            ('10 * 5', '50'),
            ('(3 + 4) * 2', '14'),
            ('100 / 4', '25'),
            ('2.5 + 7.5', '10'),
        ]
        for expr, result in calculations:
            Calculation.objects.get_or_create(
                expression=expr,
                defaults={'result': result, 'user': user}
            )

        self.stdout.write(self.style.SUCCESS('Seeding complete: 5 calculations created'))
