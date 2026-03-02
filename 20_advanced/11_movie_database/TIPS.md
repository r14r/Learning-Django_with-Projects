# Tips & Implementation Guide: Movie Database

**Level:** Advanced  
**Project:** 11_movie_database

---

## 1. Architecture Overview

Use the standard Django MTV (Model-Template-View) architecture:

```
11_movie_database/
├── manage.py
├── config/                  # Project settings package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── movie_database/  # Main application
│   ├── migrations/
│   ├── templates/
│   │   └── movie_database/
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── base.html
├── requirements.txt
└── .env.example
```

## 2. Recommended Frameworks & Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2 LTS | Web framework |
| django-crispy-forms | 2.x | Beautiful form rendering |
| crispy-bootstrap5 | 2023.x | Bootstrap 5 template pack |
| python-decouple | 3.x | Environment variable management |
| Pillow | 10.x | Image handling (if needed) |
| whitenoise | 6.x | Static file serving in production |

Install with:
```bash
pip install django django-crispy-forms crispy-bootstrap5 python-decouple whitenoise Pillow
pip freeze > requirements.txt
```

## 3. Models

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Item(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    author      = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='items'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
```

**Tips:**
- Always define `__str__` and `get_absolute_url` on models.
- Use `auto_now_add` for creation timestamps and `auto_now` for update timestamps.
- Add `class Meta: ordering` to control default queryset ordering.

## 4. Views

Prefer **Class-Based Views** for CRUD:

```python
# views.py
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Item

class ItemListView(ListView):
    model = Item
    paginate_by = 10

class ItemDetailView(DetailView):
    model = Item

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['title', 'description']

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('item-list')
```

## 5. URL Configuration

```python
# urls.py (app-level)
from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('',               views.ItemListView.as_view(),   name='list'),
    path('<int:pk>/',      views.ItemDetailView.as_view(), name='detail'),
    path('create/',        views.ItemCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='update'),
    path('<int:pk>/del/',  views.ItemDeleteView.as_view(), name='delete'),
]
```

## 6. Templates

Use template inheritance to avoid repetition:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Django App{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <!-- navigation here -->
    </nav>
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

## 7. Forms

```python
# forms.py
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters.')
        return title
```

## 8. Settings Tips

```python
# Use python-decouple for environment variables
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 9. Testing Tips

```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Item

class ItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='pass123')
        self.item = Item.objects.create(
            title='Test Item', author=self.user
        )

    def test_str(self):
        self.assertEqual(str(self.item), 'Test Item')

    def test_absolute_url(self):
        self.assertIn(str(self.item.pk), self.item.get_absolute_url())
```

## 10. Common Pitfalls

| Pitfall | Solution |
|---------|---------|
| `SECRET_KEY` committed to git | Use `.env` + `python-decouple` |
| Missing `{% csrf_token %}` | Always add to POST forms |
| N+1 query problem | Use `select_related()` / `prefetch_related()` |
| Hard-coded URLs in templates | Use `{% url 'name' %}` template tag |
| DEBUG=True in production | Use environment variables |
