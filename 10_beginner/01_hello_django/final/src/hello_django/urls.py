from django.urls import path
from . import views

app_name = 'hello_django'
urlpatterns = [
    path('',               views.MessageListView.as_view(),  name='list'),
    path('<int:pk>/',      views.MessageDetailView.as_view(), name='detail'),
    path('create/',        views.MessageCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.MessageUpdateView.as_view(), name='update'),
    path('<int:pk>/del/',  views.MessageDeleteView.as_view(), name='delete'),
]
