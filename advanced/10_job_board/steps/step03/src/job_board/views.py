from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: job_board/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: job_board/item_detail.html