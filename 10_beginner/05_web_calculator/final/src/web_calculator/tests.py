from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Calculation
from .views import safe_eval


class CalculatorTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_safe_eval_addition(self):
        self.assertEqual(safe_eval('2 + 3'), '5')

    def test_safe_eval_multiplication(self):
        self.assertEqual(safe_eval('4 * 5'), '20')

    def test_safe_eval_division_by_zero(self):
        with self.assertRaises(ValueError):
            safe_eval('1 / 0')

    def test_safe_eval_invalid_chars(self):
        with self.assertRaises(ValueError):
            safe_eval('__import__("os")')

    def test_calculator_get(self):
        resp = self.client.get(reverse('web_calculator:list'))
        self.assertEqual(resp.status_code, 200)

    def test_calculator_post_valid(self):
        resp = self.client.post(reverse('web_calculator:list'), {'expression': '10 + 5'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '15')
        self.assertEqual(Calculation.objects.count(), 1)
