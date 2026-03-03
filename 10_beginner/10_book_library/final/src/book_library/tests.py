from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book


class BookLibraryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.book = Book.objects.create(
            title='Test Book',
            author_name='Test Author',
            genre='Fiction',
        )

    def test_list_view(self):
        resp = self.client.get(reverse('book_library:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Book')

    def test_detail_view(self):
        resp = self.client.get(reverse('book_library:detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('book_library:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_book(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(reverse('book_library:create'), {
            'title': 'New Book',
            'author_name': 'New Author',
            'isbn': '',
            'genre': 'Sci-Fi',
            'published_year': 2024,
            'description': 'A great book',
            'available': True,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Book.objects.count(), 2)

    def test_genre_filter(self):
        Book.objects.create(
            title='Another Book', author_name='Author 2', genre='Non-Fiction'
        )
        resp = self.client.get(reverse('book_library:list') + '?genre=Fiction')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Book')
        self.assertNotContains(resp, 'Another Book')
