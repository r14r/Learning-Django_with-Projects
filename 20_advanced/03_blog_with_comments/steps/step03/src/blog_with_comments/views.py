from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: blog_with_comments/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: blog_with_comments/item_detail.html