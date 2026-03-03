from django.contrib import admin
from .models import Category, Recipe, Ingredient


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display    = ('title', 'author', 'published', 'created_at')
    list_filter     = ('published', 'categories')
    search_fields   = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ('categories',)
    inlines             = [IngredientInline]
