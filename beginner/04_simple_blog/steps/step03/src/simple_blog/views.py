from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: simple_blog/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: simple_blog/item_detail.html