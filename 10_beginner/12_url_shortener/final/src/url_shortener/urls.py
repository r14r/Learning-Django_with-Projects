from django.urls import path

from . import views

app_name = 'url_shortener'
urlpatterns = [
    path('', views.ShortenView.as_view(), name='list'),
    path('my-urls/', views.URLListView.as_view(), name='my-urls'),
    path('<int:pk>/del/', views.URLDeleteView.as_view(), name='delete'),
    path('<str:short_code>/', views.RedirectView.as_view(), name='redirect'),
]
