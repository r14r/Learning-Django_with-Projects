from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: event_calendar/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: event_calendar/item_detail.html