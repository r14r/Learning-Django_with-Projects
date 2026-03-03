# Tips & Implementation Guide: Analytics Dashboard

## 1. Middleware

```python
# analytics_dashboard/middleware.py
class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith('/admin') and response.status_code == 200:
            PageView.objects.create(
                path        = request.path,
                method      = request.method,
                user        = request.user if request.user.is_authenticated else None,
                session_key = request.session.session_key or '',
                user_agent  = request.META.get('HTTP_USER_AGENT', ''),
                referer     = request.META.get('HTTP_REFERER', ''),
                ip_address  = request.META.get('REMOTE_ADDR'),
            )
        return response
```

Register in settings:
```python
MIDDLEWARE = [
    ...
    'analytics_dashboard.middleware.PageViewMiddleware',
]
```

## 2. Dashboard Aggregation

```python
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone

def get_daily_stats(days=30):
    since = timezone.now() - timedelta(days=days)
    return (
        PageView.objects.filter(timestamp__gte=since)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
```

## 3. Chart.js Integration

```html
<canvas id="dailyChart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('dailyChart');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: {{ labels|safe }},
        datasets: [{ label: 'Page Views', data: {{ data|safe }} }],
    }
});
</script>
```
