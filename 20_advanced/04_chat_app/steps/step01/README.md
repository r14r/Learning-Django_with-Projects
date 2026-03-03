# Step 1 – Project Setup with Django Channels

```bash
pip install django channels daphne python-decouple
django-admin startproject config .
python manage.py startapp chat_app
```

## config/asgi.py

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
})
```
