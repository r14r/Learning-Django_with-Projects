from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: movie_database/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: movie_database/item_detail.html