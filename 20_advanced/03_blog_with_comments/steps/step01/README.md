# Step 1 – Project Setup

```bash
pip install django python-decouple
django-admin startproject config .
python manage.py startapp blog_with_comments
```

## blog_with_comments/views.py

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Blog with Comments</h1>')
```
