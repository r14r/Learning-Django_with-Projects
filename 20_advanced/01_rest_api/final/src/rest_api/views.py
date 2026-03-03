from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Author, Book, Review
from .serializers import AuthorSerializer, BookSerializer, ReviewSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({'status': 'ok'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=serializer.validated_data['password'],
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset           = Author.objects.all()
    serializer_class   = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields      = ['name']


class BookViewSet(viewsets.ModelViewSet):
    queryset           = Book.objects.select_related('author', 'owner').prefetch_related('reviews')
    serializer_class   = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields   = ['genre', 'published']
    search_fields      = ['title', 'author__name']
    ordering_fields    = ['published', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class   = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_pk'])

    def perform_create(self, serializer):
        book = Book.objects.get(pk=self.kwargs['book_pk'])
        serializer.save(author=self.request.user, book=book)
