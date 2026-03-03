from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    author       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    categories   = models.ManyToManyField(Category, blank=True, related_name='recipes')
    description  = models.TextField(blank=True)
    image        = models.ImageField(upload_to='recipes/', blank=True)
    prep_time    = models.PositiveIntegerField(default=0)
    cook_time    = models.PositiveIntegerField(default=0)
    servings     = models.PositiveIntegerField(default=4)
    instructions = models.TextField()
    published    = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_book:detail', kwargs={'slug': self.slug})

    @property
    def total_time(self):
        return (self.prep_time or 0) + (self.cook_time or 0)


class Ingredient(models.Model):
    recipe   = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name     = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit     = models.CharField(max_length=50, blank=True)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.quantity} {self.unit} {self.name}'.strip()
