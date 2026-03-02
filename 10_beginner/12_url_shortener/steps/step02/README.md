# Step 2 – Models & Database

## What you'll add
A database model with Django ORM and the Django admin interface.

## url_shortener/models.py

```python
from django.db import models
from django.contrib.auth.models import User

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
```

## url_shortener/admin.py

```python
from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'created_at')
    list_filter   = ('author',)
    search_fields = ('title', 'description')
```

## Apply migrations

```bash
python manage.py makemigrations url_shortener
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin/ and create a few items.
