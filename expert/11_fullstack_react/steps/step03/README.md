# Step 3 – Templates & List / Detail Views

## What you'll add
HTML templates with Bootstrap 5 and class-based list / detail views.

## Directory structure

```
fullstack_react/
└── templates/
    └── fullstack_react/
        ├── base.html
        ├── item_list.html
        └── item_detail.html
```

## templates/base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Full-Stack with React{% endblock %}</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css">
</head>
<body>
<nav class="navbar navbar-dark bg-dark px-3">
    <a class="navbar-brand" href="/">Full-Stack with React</a>
</nav>
<div class="container mt-4">
    {% block content %}{% endblock %}
</div>
</body>
</html>
```

## fullstack_react/views.py

```python
from django.views.generic import ListView, DetailView
from .models import Item

class ItemListView(ListView):
    model        = Item
    paginate_by  = 10
    # template: fullstack_react/item_list.html

class ItemDetailView(DetailView):
    model = Item
    # template: fullstack_react/item_detail.html
```

## config/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       include('fullstack_react.urls')),
]
```

## fullstack_react/urls.py

```python
from django.urls import path
from . import views

app_name = 'fullstack_react'
urlpatterns = [
    path('',          views.ItemListView.as_view(),   name='list'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='detail'),
]
```
