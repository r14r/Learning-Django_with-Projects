from django.urls import path
from . import views

app_name = 'contact_form'
urlpatterns = [
    path('',                      views.ContactFormView.as_view(),   name='list'),
    path('success/',              views.ContactSuccessView.as_view(), name='success'),
    path('inbox/',                views.MessageListView.as_view(),    name='inbox'),
    path('inbox/<int:pk>/',       views.MessageDetailView.as_view(),  name='detail'),
    path('inbox/<int:pk>/read/',  views.MarkReadView.as_view(),       name='mark-read'),
]
