# Step 1 – Project Setup & Django Basics

## What you'll build
A minimal Django project with a working home page.

## Instructions

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install Django
pip install django python-decouple
pip freeze > requirements.txt

# 3. Create the project
django-admin startproject config .

# 4. Create the application
python manage.py startapp docker_deployment
```

## config/settings.py (relevant parts)

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY', default='change-me-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'docker_deployment',          # ← add your app
]
```

## docker_deployment/views.py

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to Docker & Kubernetes Deploy!</h1>')
```

## config/urls.py

```python
from django.contrib import admin
from django.urls import path
from docker_deployment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]
```

## Run it

```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ — you should see "Welcome to Docker & Kubernetes Deploy!"
