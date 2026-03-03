import re
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render
from .models import Calculation
from .forms import CalculatorForm


def safe_eval(expression):
    """Evaluate a mathematical expression safely."""
    # Only allow digits, operators, spaces, dots, and parentheses
    if not re.match(r'^[\d\s\+\-\*\/\.\(\)]+$', expression):
        raise ValueError('Invalid characters in expression')
    if len(expression) > 100:
        raise ValueError('Expression too long')
    try:
        result = eval(expression, {'__builtins__': {}}, {})
        return str(round(float(result), 10)).rstrip('0').rstrip('.')
    except ZeroDivisionError:
        raise ValueError('Division by zero')
    except Exception:
        raise ValueError('Invalid expression')


class CalculatorView(View):
    template_name = 'web_calculator/item_list.html'

    def get(self, request):
        form = CalculatorForm()
        history = Calculation.objects.all()[:10]
        return render(request, self.template_name, {'form': form, 'history': history})

    def post(self, request):
        form = CalculatorForm(request.POST)
        result = None
        error  = None
        if form.is_valid():
            expr = form.cleaned_data['expression']
            try:
                result = safe_eval(expr)
                user = request.user if request.user.is_authenticated else None
                Calculation.objects.create(expression=expr, result=result, user=user)
            except ValueError as e:
                error = str(e)
        history = Calculation.objects.all()[:10]
        return render(request, self.template_name, {'form': form, 'result': result, 'error': error, 'history': history})


class HistoryListView(ListView):
    model               = Calculation
    template_name       = 'web_calculator/item_detail.html'
    context_object_name = 'object_list'
    paginate_by         = 20
