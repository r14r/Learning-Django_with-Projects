from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to URL Shortener!</h1>')