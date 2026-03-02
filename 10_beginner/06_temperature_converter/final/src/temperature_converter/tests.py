from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Conversion
from .views import convert_temperature


class ConversionMathTests(TestCase):
    def test_convert_c_to_f(self):
        result = convert_temperature(Decimal('100'), 'C', 'F')
        self.assertAlmostEqual(float(result), 212.0, places=2)

    def test_convert_f_to_c(self):
        result = convert_temperature(Decimal('32'), 'F', 'C')
        self.assertAlmostEqual(float(result), 0.0, places=2)

    def test_convert_to_kelvin(self):
        result = convert_temperature(Decimal('0'), 'C', 'K')
        self.assertAlmostEqual(float(result), 273.15, places=2)

    def test_get_view(self):
        client = Client()
        resp = client.get(reverse('temperature_converter:list'))
        self.assertEqual(resp.status_code, 200)

    def test_post_valid(self):
        client = Client()
        resp = client.post(reverse('temperature_converter:list'), {
            'value_in': '100',
            'unit_in': 'C',
            'unit_out': 'F',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Conversion.objects.count(), 1)
