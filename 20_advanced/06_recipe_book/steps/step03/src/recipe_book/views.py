from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Recipe, Category


class RecipeListView(ListView):
    template_name       = 'recipe_book/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by         = 12

    def get_queryset(self):
        qs   = Recipe.objects.filter(published=True).select_related('author').prefetch_related('categories')
        slug = self.kwargs.get('slug')
        if slug:
            cat = get_object_or_404(Category, slug=slug)
            qs  = qs.filter(categories=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class RecipeDetailView(DetailView):
    model         = Recipe
    slug_field    = 'slug'
    template_name = 'recipe_book/recipe_detail.html'