from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to E-Commerce Store!</h1>')