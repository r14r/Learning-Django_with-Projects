from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: analytics_dashboard/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: analytics_dashboard/item_detail.html