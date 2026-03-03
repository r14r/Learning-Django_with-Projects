from django.urls import path

from . import views

app_name = 'grade_tracker'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
    path('create/', views.CourseCreateView.as_view(), name='create'),
    path('<int:pk>/del/', views.CourseDeleteView.as_view(), name='delete'),
    path('<int:course_pk>/grade/add/', views.GradeCreateView.as_view(), name='grade-add'),
    path('grade/<int:pk>/del/', views.GradeDeleteView.as_view(), name='grade-delete'),
]
