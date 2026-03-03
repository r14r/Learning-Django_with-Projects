from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Hotel Booking</h1>')
