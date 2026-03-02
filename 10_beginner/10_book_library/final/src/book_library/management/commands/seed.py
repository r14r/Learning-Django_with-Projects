from django.core.management.base import BaseCommand
from book_library.models import Book


class Command(BaseCommand):
    help = 'Seed the database with classic books'

    def handle(self, *args, **kwargs):
        books = [
            {
                'title': 'Pride and Prejudice',
                'author_name': 'Jane Austen',
                'isbn': '9780141439518',
                'genre': 'Romance',
                'published_year': 1813,
                'description': 'A romantic novel of manners.',
            },
            {
                'title': 'To Kill a Mockingbird',
                'author_name': 'Harper Lee',
                'isbn': '9780061935466',
                'genre': 'Fiction',
                'published_year': 1960,
                'description': 'A story of racial injustice and moral growth.',
            },
            {
                'title': '1984',
                'author_name': 'George Orwell',
                'isbn': '9780451524935',
                'genre': 'Dystopian',
                'published_year': 1949,
                'description': 'A dystopian novel about totalitarianism.',
            },
            {
                'title': 'The Great Gatsby',
                'author_name': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'genre': 'Fiction',
                'published_year': 1925,
                'description': 'A critique of the American Dream.',
            },
            {
                'title': 'Brave New World',
                'author_name': 'Aldous Huxley',
                'isbn': '9780060850524',
                'genre': 'Dystopian',
                'published_year': 1932,
                'description': 'A dystopian vision of a future society.',
            },
        ]
        for data in books:
            Book.objects.get_or_create(title=data['title'], defaults=data)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(books)} classic books.'))
