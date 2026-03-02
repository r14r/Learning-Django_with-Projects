from django.urls import path

from . import views

app_name = 'notes_app'
urlpatterns = [
    path('', views.NoteListView.as_view(), name='list'),
    path('<int:pk>/', views.NoteDetailView.as_view(), name='detail'),
    path('create/', views.NoteCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.NoteUpdateView.as_view(), name='update'),
    path('<int:pk>/del/', views.NoteDeleteView.as_view(), name='delete'),
    path('<int:pk>/pin/', views.toggle_pin, name='pin'),
]
