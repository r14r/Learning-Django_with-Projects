from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: quiz_app/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: quiz_app/item_detail.html