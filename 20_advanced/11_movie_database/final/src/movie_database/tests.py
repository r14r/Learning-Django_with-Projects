from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Genre, Person, Movie, Rating, Review, Watchlist


class MovieDBTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user   = User.objects.create_user('alice', password='pass')
        self.genre  = Genre.objects.create(name='Action', slug='action')
        self.person = Person.objects.create(name='John Doe')
        self.movie  = Movie.objects.create(
            title='Test Movie', slug='test-movie', year=2020, director=self.person
        )
        self.movie.genres.add(self.genre)

    def test_list_view(self):
        resp = self.client.get(reverse('movie_database:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Movie')

    def test_detail_view(self):
        resp = self.client.get(reverse('movie_database:detail', kwargs={'slug': 'test-movie'}))
        self.assertEqual(resp.status_code, 200)

    def test_rate_movie(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('movie_database:rate', kwargs={'pk': self.movie.pk}), {'score': 8})
        self.assertEqual(Rating.objects.count(), 1)

    def test_rate_upsert(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('movie_database:rate', kwargs={'pk': self.movie.pk}), {'score': 8})
        self.client.post(reverse('movie_database:rate', kwargs={'pk': self.movie.pk}), {'score': 5})
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().score, 5)

    def test_watchlist_toggle(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('movie_database:watchlist', kwargs={'pk': self.movie.pk}))
        self.assertEqual(Watchlist.objects.count(), 1)
        self.client.post(reverse('movie_database:watchlist', kwargs={'pk': self.movie.pk}))
        self.assertEqual(Watchlist.objects.count(), 0)

    def test_genre_filter(self):
        resp = self.client.get(reverse('movie_database:genre', kwargs={'slug': 'action'}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Movie')
