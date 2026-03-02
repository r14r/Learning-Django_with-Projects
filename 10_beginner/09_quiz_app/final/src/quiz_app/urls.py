from django.urls import path
from . import views

app_name = 'quiz_app'
urlpatterns = [
    path('',              views.QuizListView.as_view(),   name='list'),
    path('<int:pk>/',     views.QuizDetailView.as_view(), name='detail'),
    path('<int:pk>/take/', views.TakeQuizView.as_view(),  name='take'),
    path('result/<int:pk>/', views.QuizResultView.as_view(), name='result'),
    path('create/',       views.QuizCreateView.as_view(), name='create'),
    path('<int:pk>/del/', views.QuizDeleteView.as_view(), name='delete'),
]
