from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Event, Category


class UpcomingEventsView(ListView):
    template_name       = 'event_calendar/event_list.html'
    context_object_name = 'events'
    paginate_by         = 10

    def get_queryset(self):
        qs = Event.objects.filter(is_public=True, start__gte=timezone.now()).select_related('category')
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category__id=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class EventDetailView(DetailView):
    model         = Event
    slug_field    = 'slug'
    template_name = 'event_calendar/event_detail.html'