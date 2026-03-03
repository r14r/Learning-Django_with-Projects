from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register('authors', views.AuthorViewSet)
router.register('books',   views.BookViewSet)
router.register(r'books/(?P<book_pk>[^/.]+)/reviews', views.ReviewViewSet,
                basename='book-reviews')

urlpatterns = [
    path('health/',        views.health,       name='health'),
    path('auth/register/', views.register,     name='register'),
    path('auth/login/',    obtain_auth_token,  name='login'),
    path('', include(router.urls)),
]