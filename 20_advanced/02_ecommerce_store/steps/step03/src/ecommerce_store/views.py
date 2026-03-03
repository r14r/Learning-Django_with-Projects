from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Category, Product


class ProductListView(ListView):
    model               = Product
    template_name       = 'ecommerce_store/product_list.html'
    context_object_name = 'products'
    paginate_by         = 12

    def get_queryset(self):
        qs   = Product.objects.filter(available=True).select_related('category')
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductDetailView(DetailView):
    model         = Product
    slug_field    = 'slug'
    template_name = 'ecommerce_store/product_detail.html'