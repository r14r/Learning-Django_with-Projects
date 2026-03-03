from django.views.generic import ListView, DetailView
from .models import Room
from .forms import SearchForm


class RoomListView(ListView):
    model               = Room
    template_name       = 'hotel_booking/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        qs = Room.objects.filter(available=True)
        rt = self.request.GET.get('room_type')
        if rt:
            qs = qs.filter(room_type=rt)
        cap = self.request.GET.get('capacity')
        if cap:
            qs = qs.filter(capacity__gte=cap)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SearchForm(self.request.GET or None)
        return ctx


class RoomDetailView(DetailView):
    model         = Room
    template_name = 'hotel_booking/room_detail.html'