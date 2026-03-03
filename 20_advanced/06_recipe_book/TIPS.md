# Tips & Implementation Guide: Recipe Book

## 1. Ingredient Inline Formset

Use Django inline formsets to manage multiple ingredients on a single form:

```python
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient

IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient,
    fields=['name', 'quantity', 'unit', 'order'],
    extra=3,
    can_delete=True,
)
```

In the view:
```python
def recipe_create(request):
    if request.method == 'POST':
        form    = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            formset.instance = recipe
            formset.save()
            return redirect(recipe.get_absolute_url())
    else:
        form    = RecipeForm()
        formset = IngredientFormSet()
    return render(request, 'recipe_book/recipe_form.html', {'form': form, 'formset': formset})
```

## 2. Total Time Property

```python
@property
def total_time(self):
    return (self.prep_time or 0) + (self.cook_time or 0)
```

## 3. Search Query

```python
def get_queryset(self):
    qs = Recipe.objects.filter(published=True)
    q  = self.request.GET.get('q')
    if q:
        qs = qs.filter(
            models.Q(title__icontains=q) | models.Q(ingredients__name__icontains=q)
        ).distinct()
    return qs
```
