from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to Todo List!</h1>')