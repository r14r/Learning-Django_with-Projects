from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Author, Book, Review


class AuthAPITest(APITestCase):
    def test_register(self):
        resp = self.client.post('/api/auth/register/', {
            'username': 'alice', 'password': 'secret123'
        })
        self.assertEqual(resp.status_code, 201)
        self.assertIn('token', resp.data)


class BookAPITest(APITestCase):
    def setUp(self):
        self.user   = User.objects.create_user('alice', password='pass')
        self.token  = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='J.K. Rowling')
        self.book   = Book.objects.create(
            title='Harry Potter', author=self.author,
            genre='Fantasy', published=1997, owner=self.user
        )

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_books_public(self):
        resp = self.client.get('/api/books/')
        self.assertEqual(resp.status_code, 200)

    def test_book_detail(self):
        resp = self.client.get(f'/api/books/{self.book.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], 'Harry Potter')

    def test_create_book_requires_auth(self):
        resp = self.client.post('/api/books/', {'title': 'X'})
        self.assertEqual(resp.status_code, 401)

    def test_create_book(self):
        self.auth()
        resp = self.client.post('/api/books/', {
            'title': 'New Book', 'author': self.author.pk,
            'genre': 'Drama', 'published': 2020,
        })
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_owner_can_update(self):
        self.auth()
        resp = self.client.patch(f'/api/books/{self.book.pk}/', {'title': 'Updated'})
        self.assertEqual(resp.status_code, 200)

    def test_owner_can_delete(self):
        self.auth()
        resp = self.client.delete(f'/api/books/{self.book.pk}/')
        self.assertEqual(resp.status_code, 204)

    def test_non_owner_cannot_delete(self):
        other = User.objects.create_user('bob', password='pass')
        t     = Token.objects.create(user=other)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {t.key}')
        resp  = self.client.delete(f'/api/books/{self.book.pk}/')
        self.assertEqual(resp.status_code, 403)

    def test_search_by_title(self):
        resp = self.client.get('/api/books/?search=Harry')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_genre(self):
        resp = self.client.get('/api/books/?genre=Fantasy')
        self.assertEqual(resp.status_code, 200)
