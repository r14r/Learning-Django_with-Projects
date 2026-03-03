from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import WeatherSearch


class WeatherDisplayTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')

    def test_get_view(self):
        resp = self.client.get(reverse('weather:list'))
        self.assertEqual(resp.status_code, 200)

    def test_post_without_api(self):
        with patch('weather.views.get_weather', return_value=None):
            resp = self.client.post(
                reverse('weather:list'),
                {'city': 'UnknownCity'},
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(WeatherSearch.objects.count(), 0)

    def test_post_with_mock_data(self):
        mock_data = {'temperature': 22.5, 'condition': 'Sunny', 'humidity': 60}
        with patch('weather.views.get_weather', return_value=mock_data):
            resp = self.client.post(
                reverse('weather:list'),
                {'city': 'London'},
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(WeatherSearch.objects.count(), 1)
        search = WeatherSearch.objects.first()
        self.assertEqual(search.city, 'London')
        self.assertEqual(search.condition, 'Sunny')

    def test_history_requires_login(self):
        resp = self.client.get(reverse('weather:detail'))
        self.assertNotEqual(resp.status_code, 200)

    def test_weather_search_str(self):
        search = WeatherSearch(city='Paris', condition='Cloudy')
        self.assertEqual(str(search), 'Paris - Cloudy')
