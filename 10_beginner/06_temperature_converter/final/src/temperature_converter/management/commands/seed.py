from decimal import Decimal
from django.core.management.base import BaseCommand
from temperature_converter.models import Conversion
from temperature_converter.views import convert_temperature


class Command(BaseCommand):
    help = 'Seed the database with sample conversions'

    def handle(self, *args, **kwargs):
        samples = [
            (Decimal('100'), 'C', 'F'),
            (Decimal('32'),  'F', 'C'),
            (Decimal('0'),   'C', 'K'),
            (Decimal('373.15'), 'K', 'C'),
            (Decimal('-40'), 'F', 'C'),
        ]
        for value_in, unit_in, unit_out in samples:
            value_out = convert_temperature(value_in, unit_in, unit_out)
            Conversion.objects.create(
                value_in=value_in,
                unit_in=unit_in,
                value_out=value_out,
                unit_out=unit_out,
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(samples)} conversions.'))
