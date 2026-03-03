# Step 4 – Write Endpoints, Auth & Custom Permission

## What you'll add
Token authentication, user registration, full CRUD, and an `IsOwnerOrReadOnly`
permission class.

## rest_api/permissions.py

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

## rest_api/views.py  (full CRUD + auth)

```python
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .permissions import IsOwnerOrReadOnly
from .serializers import BookSerializer, AuthorSerializer, ReviewSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user  = User.objects.create_user(**serializer.validated_data)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(viewsets.ModelViewSet):
    queryset           = Book.objects.select_related('author', 'owner').prefetch_related('reviews')
    serializer_class   = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    search_fields      = ['title', 'author__name']
    filterset_fields   = ['genre', 'published']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```
