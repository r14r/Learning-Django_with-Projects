from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Real-Time Chat</h1>')
