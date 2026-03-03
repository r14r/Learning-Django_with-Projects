from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Book.objects.select_related('author', 'owner').prefetch_related('reviews')
    serializer_class = BookSerializer
    search_fields    = ['title', 'author__name']
    filterset_fields = ['genre', 'published']
