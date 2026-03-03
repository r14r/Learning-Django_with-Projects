from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Room, Message
from .forms import RoomForm


class RoomListView(LoginRequiredMixin, ListView):
    model               = Room
    template_name       = 'chat_app/room_list.html'
    context_object_name = 'rooms'


class RoomCreateView(LoginRequiredMixin, CreateView):
    model         = Room
    form_class    = RoomForm
    template_name = 'chat_app/room_form.html'
    success_url   = reverse_lazy('chat_app:list')


def room_view(request, slug):
    room     = get_object_or_404(Room, slug=slug)
    messages = list(room.messages.select_related('author').order_by('-timestamp')[:50])
    messages.reverse()
    return render(request, 'chat_app/room.html', {
        'room': room, 'messages': messages,
    })