import json
import urllib.request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .forms import WeatherSearchForm
from .models import WeatherSearch


def get_weather(city):
    url = f'https://wttr.in/{city}?format=j1'
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        current = data['current_condition'][0]
        return {
            'temperature': float(current['temp_C']),
            'condition': current['weatherDesc'][0]['value'],
            'humidity': int(current['humidity']),
        }
    except Exception:
        return None


class WeatherView(View):
    template_name = 'weather_display/item_list.html'

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
                WeatherSearch.objects.create(
                    city=city,
                    temperature=weather_data['temperature'],
                    condition=weather_data['condition'],
                    humidity=weather_data['humidity'],
                    user=user,
                )
            else:
                error = f"Could not retrieve weather for '{city}'. Please try again."
        return render(request, self.template_name, {
            'form': form,
            'weather_data': weather_data,
            'city': form.cleaned_data.get('city', '') if form.is_valid() else '',
            'error': error,
        })


class SearchHistoryView(LoginRequiredMixin, ListView):
    model = WeatherSearch
    template_name = 'weather_display/item_detail.html'
    context_object_name = 'searches'
    paginate_by = 20
