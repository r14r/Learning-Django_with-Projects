from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models as db_models
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Recipe, Category, Ingredient
from .forms import RecipeForm

IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient,
    fields=['name', 'quantity', 'unit', 'order'],
    extra=3, can_delete=True,
)


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
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                db_models.Q(title__icontains=q) | db_models.Q(ingredients__name__icontains=q)
            ).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class RecipeDetailView(DetailView):
    model         = Recipe
    slug_field    = 'slug'
    template_name = 'recipe_book/recipe_detail.html'


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form    = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe         = form.save(commit=False)
            recipe.author  = request.user
            recipe.save()
            form.save_m2m()
            formset.instance = recipe
            formset.save()
            return redirect(recipe.get_absolute_url())
    else:
        form    = RecipeForm()
        formset = IngredientFormSet()
    return render(request, 'recipe_book/recipe_form.html', {'form': form, 'formset': formset})


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    if request.method == 'POST':
        form    = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(recipe.get_absolute_url())
    else:
        form    = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe)
    return render(request, 'recipe_book/recipe_form.html', {'form': form, 'formset': formset})


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model         = Recipe
    slug_field    = 'slug'
    template_name = 'recipe_book/recipe_confirm_delete.html'
    success_url   = reverse_lazy('recipe_book:my-recipes')


class MyRecipesView(LoginRequiredMixin, ListView):
    template_name       = 'recipe_book/my_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)