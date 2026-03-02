# Step 5 – Authentication, Tests & Deployment Prep

## What you'll add
User login/logout, a full test suite and production-ready settings.

## config/urls.py  (add auth URLs)

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',          include('ml_integration.urls')),
]
```

## registration/login.html  (template for built-in login view)

```html
{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-4">
    <h2>Login</h2>
    <form method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <button class="btn btn-primary w-100" type="submit">Login</button>
    </form>
  </div>
</div>
{% endblock %}
```

## ml_integration/tests.py

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Item

class ItemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester', password='secret123'
        )
        self.item = Item.objects.create(
            title='Test Item',
            description='A test item',
            author=self.user,
        )

    def test_list_view(self):
        resp = self.client.get(reverse('ml_integration:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Item')

    def test_detail_view(self):
        resp = self.client.get(
            reverse('ml_integration:detail', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('ml_integration:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_item(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('ml_integration:create'),
            {'title': 'New Item', 'description': 'Created in test'},
        )
        self.assertEqual(Item.objects.count(), 2)

    def test_delete_item(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('ml_integration:delete', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(Item.objects.count(), 0)
```

## Run tests

```bash
python manage.py test ml_integration
```

## .env.example

```
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

## requirements.txt

```
Django==4.2.11
python-decouple==3.8
django-crispy-forms==2.1
crispy-bootstrap5==2024.2
whitenoise==6.6.0
Pillow==10.3.0
```

## Deployment checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` via environment variable
- [ ] `ALLOWED_HOSTS` configured
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Database migrated: `python manage.py migrate`
- [ ] Superuser created: `python manage.py createsuperuser`
