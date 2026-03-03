from decimal import Decimal
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Booking
from .forms import BookingForm, SearchForm


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


@login_required
def book_view(request, pk):
    room = get_object_or_404(Room, pk=pk, available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in  = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            conflict = Booking.objects.filter(
                room=room, status__in=['pending', 'confirmed']
            ).exclude(check_out__lte=check_in).exclude(check_in__gte=check_out)
            if conflict.exists():
                messages.error(request, 'Room is not available for those dates.')
            else:
                nights = (check_out - check_in).days
                total  = Decimal(nights) * room.price_night
                b = form.save(commit=False)
                b.room        = room
                b.guest       = request.user
                b.total_price = total
                b.status      = 'confirmed'
                b.save()
                return redirect('hotel_booking:my-bookings')
    else:
        form = BookingForm()
    return render(request, 'hotel_booking/book.html', {'room': room, 'form': form})


@login_required
def guest_dashboard(request):
    bookings = Booking.objects.filter(guest=request.user).select_related('room')
    return render(request, 'hotel_booking/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    b = get_object_or_404(Booking, pk=pk, guest=request.user)
    if request.method == 'POST' and b.status != 'cancelled':
        b.status = 'cancelled'
        b.save()
    return redirect('hotel_booking:my-bookings')