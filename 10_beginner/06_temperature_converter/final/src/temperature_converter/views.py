from decimal import Decimal
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .models import Conversion
from .forms import ConverterForm


def convert_temperature(value, unit_in, unit_out):
    """Convert temperature between Celsius, Fahrenheit and Kelvin."""
    value = Decimal(str(value))
    if unit_in == unit_out:
        return value
    # Convert to Celsius first
    if unit_in == 'F':
        celsius = (value - Decimal('32')) * Decimal('5') / Decimal('9')
    elif unit_in == 'K':
        celsius = value - Decimal('273.15')
    else:
        celsius = value
    # Convert from Celsius to target
    if unit_out == 'F':
        return celsius * Decimal('9') / Decimal('5') + Decimal('32')
    elif unit_out == 'K':
        return celsius + Decimal('273.15')
    else:
        return celsius


class ConverterView(View):
    template_name = 'temperature_converter/item_list.html'

    def get(self, request):
        form = ConverterForm()
        recent = Conversion.objects.all()[:10]
        return render(request, self.template_name, {'form': form, 'recent': recent})

    def post(self, request):
        form = ConverterForm(request.POST)
        if form.is_valid():
            value_in = form.cleaned_data['value_in']
            unit_in  = form.cleaned_data['unit_in']
            unit_out = form.cleaned_data['unit_out']
            value_out = convert_temperature(value_in, unit_in, unit_out)
            conversion = Conversion.objects.create(
                value_in=value_in,
                unit_in=unit_in,
                value_out=value_out,
                unit_out=unit_out,
                user=request.user if request.user.is_authenticated else None,
            )
            recent = Conversion.objects.all()[:10]
            return render(request, self.template_name, {
                'form': form,
                'result': conversion,
                'recent': recent,
            })
        recent = Conversion.objects.all()[:10]
        return render(request, self.template_name, {'form': form, 'recent': recent})


class HistoryListView(ListView):
    model = Conversion
    template_name = 'temperature_converter/item_detail.html'
    context_object_name = 'conversions'
    paginate_by = 20
