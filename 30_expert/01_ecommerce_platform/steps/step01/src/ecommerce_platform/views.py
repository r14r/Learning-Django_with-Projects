from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to Full E-Commerce Platform!</h1>')