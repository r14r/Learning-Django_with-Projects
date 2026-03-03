import json
import urllib.request

import requests

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .forms import WeatherSearchForm
from .models import WeatherSearch

def get_location(name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": name,
        "count": 5,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
    
def get_coordinates(name: str):
    results = get_location(name)

    locations = results.get("results", [])

    for i, loc in enumerate(locations):
        print(f"{i}: {loc['name']}, {loc.get('country')} "
          f"(lat={loc['latitude']}, lon={loc['longitude']})")
    
    
def get_weather(city):
    coordinates = get_location(city)

    coordinate = coordinates['results'][0]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coordinate['latitude'],
        "longitude": coordinate['longitude'],
        "current_weather": True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("ERROR: get_weather ", e)
        return None


class WeatherView(View):
    template_name = 'weather/item_list.html'

    def get(self, request):
        form = WeatherSearchForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = WeatherSearchForm(request.POST)
        weather_data = None
        error = None
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather(city)
            if weather_data:
                user = request.user if request.user.is_authenticated else None

                weather = weather_data['current_weather']
                WeatherSearch.objects.create(
                    city=city,
                    temperature=weather['temperature'],
                    windspeed=weather['windspeed'],
                    winddirection=weather['winddirection'],
                    user=user,
                )
            else:
                error = f"Could not retrieve weather for '{city}'. Please try again."
        return render(request, self.template_name, {
            'form': form,
            'weather': weather,
            'city': form.cleaned_data.get('city', '') if form.is_valid() else '',
            'error': error,
        })


class SearchHistoryView(LoginRequiredMixin, ListView):
    model = WeatherSearch
    template_name = 'weather/item_detail.html'
    context_object_name = 'searches'
    paginate_by = 20
