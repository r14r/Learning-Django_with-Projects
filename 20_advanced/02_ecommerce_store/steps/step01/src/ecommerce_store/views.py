from django.shortcuts import render

def home(request):
    return render(request, 'ecommerce_store/home.html', {})
