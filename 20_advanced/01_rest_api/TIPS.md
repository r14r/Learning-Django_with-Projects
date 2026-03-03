# Tips & Implementation Guide: REST API with DRF

**Level:** Advanced  
**Project:** 01_rest_api

---

## 1. Architecture Overview

```
01_rest_api/
├── config/
│   ├── settings.py
│   └── urls.py
├── rest_api/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py      ← new in DRF projects
│   ├── views.py            ← ModelViewSet / APIView
│   ├── urls.py             ← DefaultRouter
│   ├── permissions.py      ← custom IsOwnerOrReadOnly
│   ├── filters.py          ← django-filter FilterSet
│   └── tests.py
├── requirements.txt
└── .env.example
```

## 2. Install dependencies

```bash
pip install django djangorestframework django-filter python-decouple Pillow
pip freeze > requirements.txt
```

## 3. Settings additions

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'rest_api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## 4. Models

```python
class Author(models.Model):
    name = models.CharField(max_length=200)
    bio  = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Book(models.Model):
    title       = models.CharField(max_length=300)
    author      = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre       = models.CharField(max_length=100)
    published   = models.IntegerField()
    description = models.TextField(blank=True)
    cover       = models.ImageField(upload_to='covers/', blank=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Review(models.Model):
    book    = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    rating  = models.PositiveSmallIntegerField()  # 1–5
    body    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

## 5. Serializers

```python
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model  = Review
        fields = ['id', 'author', 'rating', 'body', 'created_at']

class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    owner   = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model  = Book
        fields = ['id', 'title', 'author', 'genre', 'published',
                  'description', 'owner', 'reviews', 'created_at']
```

## 6. ViewSets & Router

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset         = Book.objects.all().select_related('author', 'owner')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields   = ['genre', 'published']
    search_fields      = ['title', 'author__name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# urls.py
router = DefaultRouter()
router.register('books',   BookViewSet)
router.register('authors', AuthorViewSet)
```

## 7. Custom Permission

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

## 8. Auth endpoints

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=201)
    return Response(serializer.errors, status=400)
```

## 9. Testing

```python
from rest_framework.test import APITestCase

class BookAPITest(APITestCase):
    def test_list_books_unauthenticated(self):
        resp = self.client.get('/api/books/')
        self.assertEqual(resp.status_code, 200)

    def test_create_book_requires_auth(self):
        resp = self.client.post('/api/books/', {'title': 'X'})
        self.assertEqual(resp.status_code, 401)
```

## 10. Common Pitfalls

| Pitfall | Solution |
|---------|---------|
| Forgetting `perform_create` | Always set `owner` from `request.user` |
| N+1 queries | Use `select_related` and `prefetch_related` |
| Writable nested serializers | Use `SerializerMethodField` or custom `create` |
| Missing `format_suffix_patterns` | Include DRF URLs properly in `urls.py` |
