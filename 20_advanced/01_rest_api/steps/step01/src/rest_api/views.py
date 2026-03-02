from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to REST API with DRF!</h1>')