from django.urls import path
from . import views

app_name = 'newsletter_system'
urlpatterns = [
    path('subscribe/',                   views.subscribe_view,              name='subscribe'),
    path('confirm/<uuid:token>/',        views.confirm_view,                name='confirm'),
    path('unsubscribe/<uuid:token>/',    views.unsubscribe_view,            name='unsubscribe'),
    path('campaigns/',                   views.CampaignListView.as_view(),  name='campaign-list'),
    path('campaigns/create/',            views.CampaignCreateView.as_view(), name='campaign-create'),
    path('campaigns/<int:pk>/send/',     views.send_campaign,               name='send'),
]
