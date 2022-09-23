from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from .utils import get_rates, str_to_class, DESIRED_CURRENCIES
from .models import Euro, Real, Yen


class HomeView(generic.ListView):
    template_name = 'exchange/home.html'
    context_object_name = 'response'

    def get_queryset(self):
        get_rates(base="USD", date_start=timezone.now())
        e = Euro.objects.order_by('exc_date').last()
        r = Real.objects.order_by('exc_date').last()
        y = Yen.objects.order_by('exc_date').last()
        return [('EUR', e.value), ('BRL', r.value), ('JPY', y.value)]


def full_chart(request, currency):
    c = str_to_class(currency).objects.values('exc_date', 'value')

    iso_code = [iso_code for iso_code in DESIRED_CURRENCIES if DESIRED_CURRENCIES[iso_code] == currency.capitalize()].pop()
    rates = [[item['exc_date'].timestamp()*1000, item['value']] for item in c]
    sorted_rates = sorted(rates, key=lambda rate: rate[0])
    context = {
        'iso_code': iso_code,
        'currency': DESIRED_CURRENCIES[iso_code],
        'rates': sorted_rates,
    }

    return render(request, 'exchange/chart.html', context)


def time_chart(request, currency):
    starting_date = datetime.strptime(request.POST['starting-date'], '%Y-%m-%d')
    ending_date = datetime.strptime(request.POST['ending-date'], '%Y-%m-%d')
    iso_code = [iso_code for iso_code in DESIRED_CURRENCIES if DESIRED_CURRENCIES[iso_code] == currency.capitalize()].pop()

    context = get_rates(
        base="USD",
        date_start=starting_date,
        date_stop=ending_date
    )
    if context:
        context['currency'] = currency
        return render(request, 'exchange/chart.html', context)

    c = str_to_class(currency).objects.filter(
        exc_date__range=[starting_date.date().isoformat(), ending_date.date().isoformat()]
        ).values('exc_date', 'value')

    rates = [[item['exc_date'].timestamp()*1000, item['value']] for item in c]
    sorted_rates = sorted(rates, key=lambda rate: rate[0])
    context = {
        'iso_code': iso_code,
        'currency': DESIRED_CURRENCIES[iso_code],
        'rates': sorted_rates,
    }
    return render(request, 'exchange/chart.html', context)
