from django.urls import path
from . import views

app_name = 'invoice_generator'
urlpatterns = [
    path('',                   views.InvoiceListView.as_view(),  name='list'),
    path('invoice/<int:pk>/',  views.InvoiceDetailView.as_view(), name='detail'),
    path('clients/',           views.ClientListView.as_view(),   name='clients'),
]