from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Recipe, Ingredient


class RecipeTests(TestCase):
    def setUp(self):
        self.client   = Client()
        self.user     = User.objects.create_user('alice', password='pass')
        self.category = Category.objects.create(name='Italian', slug='italian')
        self.recipe   = Recipe.objects.create(
            title='Pasta Carbonara', slug='pasta-carbonara',
            author=self.user, instructions='...', published=True,
        )
        self.recipe.categories.add(self.category)
        Ingredient.objects.create(recipe=self.recipe, name='Pasta', quantity=200, unit='g')

    def test_list_view(self):
        resp = self.client.get(reverse('recipe_book:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Pasta Carbonara')

    def test_draft_hidden(self):
        Recipe.objects.create(
            title='Draft Recipe', slug='draft', author=self.user,
            instructions='...', published=False,
        )
        resp = self.client.get(reverse('recipe_book:list'))
        self.assertNotContains(resp, 'Draft Recipe')

    def test_detail_view(self):
        resp = self.client.get(
            reverse('recipe_book:detail', kwargs={'slug': 'pasta-carbonara'})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Pasta')

    def test_category_filter(self):
        resp = self.client.get(
            reverse('recipe_book:category', kwargs={'slug': 'italian'})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Pasta Carbonara')

    def test_create_requires_login(self):
        resp = self.client.get(reverse('recipe_book:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_total_time(self):
        self.recipe.prep_time = 10
        self.recipe.cook_time = 20
        self.assertEqual(self.recipe.total_time, 30)
