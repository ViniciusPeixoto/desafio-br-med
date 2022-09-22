from django.shortcuts import render
from django.views import generic
from .utils import get_current_rates, str_to_class
from .models import Euro, Real, Yen


class HomeView(generic.ListView):
    template_name = 'exchange/home.html'
    context_object_name = 'response'

    def get_queryset(self):
        return get_current_rates()


def chart(request, currency):
    c = str_to_class(currency).objects.values('exc_date', 'value')

    rates = [[item['exc_date'].timestamp()*1000, item['value']] for item in c]
    iso_code = str_to_class(currency).objects.last().iso_code
    context = {'currency': iso_code, 'rates': rates}

    return render(request, 'exchange/chart.html', context)
