from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('authors', views.AuthorViewSet)
router.register('books',   views.BookViewSet)

urlpatterns = [
    path('health/', views.health, name='health'),
    path('', include(router.urls)),
]