from django.http import JsonResponse
from django.utils import timezone
from .models import PageView, Event
import json


def record_event(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            Event.objects.create(
                name        = body.get('name', 'unknown')[:100],
                properties  = body.get('properties', {}),
                session_key = (request.session.session_key or '')[:40],
            )
        except (json.JSONDecodeError, Exception):
            pass
    return JsonResponse({'status': 'ok'})