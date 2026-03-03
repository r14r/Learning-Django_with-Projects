# Step 1 – Project Setup & Home Page

```bash
pip install django python-decouple Pillow
django-admin startproject config .
python manage.py startapp ecommerce_store
```

## ecommerce_store/views.py

```python
from django.shortcuts import render

def home(request):
    return render(request, 'ecommerce_store/home.html', {})
```
