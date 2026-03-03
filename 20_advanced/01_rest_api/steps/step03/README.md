# Step 3 – Serializers & Read-Only Endpoints

## What you'll add
DRF serializers and read-only list/detail endpoints via `ModelViewSet`.

## rest_api/serializers.py

```python
from rest_framework import serializers
from .models import Author, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Author
        fields = ['id', 'name', 'bio', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model  = Review
        fields = ['id', 'author', 'rating', 'body', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    reviews     = ReviewSerializer(many=True, read_only=True)
    owner       = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model  = Book
        fields = [
            'id', 'title', 'author', 'author_name', 'genre',
            'published', 'description', 'owner', 'reviews', 'created_at',
        ]
```

## rest_api/views.py

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
```

## rest_api/urls.py

```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('authors', views.AuthorViewSet)
router.register('books',   views.BookViewSet)

urlpatterns = router.urls
```
