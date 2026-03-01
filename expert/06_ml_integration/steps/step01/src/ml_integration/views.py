from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to ML Model Integration!</h1>')