import calendar
from collections import defaultdict
from datetime import date
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event, Registration, Category
from .forms import EventForm


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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['registered'] = Registration.objects.filter(
                event=self.object, attendee=self.request.user
            ).exists()
        return ctx


class EventCreateView(LoginRequiredMixin, CreateView):
    model         = Event
    form_class    = EventForm
    template_name = 'event_calendar/event_form.html'
    success_url   = reverse_lazy('event_calendar:list')

    def form_valid(self, form):
        form.instance.organiser = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model         = Event
    form_class    = EventForm
    template_name = 'event_calendar/event_form.html'
    success_url   = reverse_lazy('event_calendar:list')


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model         = Event
    template_name = 'event_calendar/event_confirm_delete.html'
    success_url   = reverse_lazy('event_calendar:list')


@login_required
def register_view(request, slug):
    event = get_object_or_404(Event, slug=slug, is_public=True)
    if Registration.objects.filter(event=event, attendee=request.user).exists():
        messages.warning(request, 'You are already registered.')
    elif event.is_full:
        messages.error(request, 'Sorry, this event is full.')
    else:
        Registration.objects.create(event=event, attendee=request.user)
        messages.success(request, 'Successfully registered!')
    return redirect(event.get_absolute_url())


@login_required
def cancel_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    Registration.objects.filter(event=event, attendee=request.user).delete()
    messages.info(request, 'Registration cancelled.')
    return redirect(event.get_absolute_url())


class MyEventsView(LoginRequiredMixin, ListView):
    template_name       = 'event_calendar/my_events.html'
    context_object_name = 'registrations'

    def get_queryset(self):
        return Registration.objects.filter(
            attendee=self.request.user
        ).select_related('event').order_by('event__start')