# Step 1 – Project Setup & DRF Installation

## What you'll build
A minimal Django project with DRF installed and a single health-check endpoint.

## Instructions

```bash
pip install django djangorestframework python-decouple
django-admin startproject config .
python manage.py startapp rest_api
```

## config/settings.py additions

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_api',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}
```

## rest_api/views.py

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'message': 'REST API with DRF is running'})
```

## config/urls.py

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',   include('rest_api.urls')),
]
```

## rest_api/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health, name='health'),
]
```

## Run & test

```bash
python manage.py migrate
python manage.py runserver
curl http://127.0.0.1:8000/api/health/
# {"status": "ok", "message": "REST API with DRF is running"}
```
