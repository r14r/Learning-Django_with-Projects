from django.urls import path
from . import views

app_name = 'invoice_generator'
urlpatterns = [
    path('',                                        views.InvoiceListView.as_view(),  name='list'),
    path('invoice/<int:pk>/',                       views.InvoiceDetailView.as_view(), name='detail'),
    path('invoice/create/',                         views.invoice_create,             name='create'),
    path('invoice/<int:pk>/status/<str:status>/',   views.update_status,              name='update-status'),
    path('clients/',                                views.ClientListView.as_view(),   name='clients'),
]