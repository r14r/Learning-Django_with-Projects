import json
from datetime import timedelta
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import PageView, Event


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics_dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx   = super().get_context_data(**kwargs)
        now   = timezone.now()
        today = now.date()
        since_30 = now - timedelta(days=30)

        ctx['today_views'] = PageView.objects.filter(timestamp__date=today).count()
        ctx['week_views']  = PageView.objects.filter(timestamp__gte=now - timedelta(days=7)).count()
        ctx['month_views'] = PageView.objects.filter(timestamp__gte=since_30).count()

        daily = (
            PageView.objects.filter(timestamp__gte=since_30)
            .annotate(date=TruncDate('timestamp'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        ctx['chart_labels'] = json.dumps([str(d['date']) for d in daily])
        ctx['chart_data']   = json.dumps([d['count'] for d in daily])

        ctx['top_pages'] = (
            PageView.objects.filter(timestamp__gte=since_30)
            .values('path')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        return ctx


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


def daily_stats(request):
    since = timezone.now() - timedelta(days=30)
    data  = (
        PageView.objects.filter(timestamp__gte=since)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    return JsonResponse({'results': list(data)}, safe=False)