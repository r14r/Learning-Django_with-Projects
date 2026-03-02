from django.urls import path
from . import views

app_name = 'grade_tracker'
urlpatterns = [
    path('',               views.ItemListView.as_view(),   name='list'),
    path('<int:pk>/',      views.ItemDetailView.as_view(), name='detail'),
    path('create/',        views.ItemCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='update'),
    path('<int:pk>/del/',  views.ItemDeleteView.as_view(), name='delete'),
]