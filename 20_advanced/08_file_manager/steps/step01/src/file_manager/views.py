from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>File Upload Manager</h1>')
