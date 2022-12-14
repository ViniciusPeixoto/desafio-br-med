from datetime import datetime
from django.shortcuts import render
from django.views import generic
from .utils import get_rates, str_to_class, DESIRED_CURRENCIES
from .models import Euro, Real, Yen


class HomeView(generic.ListView):
    template_name = "exchange/home.html"
    context_object_name = "response"

    # Home page will show latest exchange rates for desired currencies.
    def get_queryset(self):
        get_rates(base="USD", date_start=datetime.today())
        return [
            (iso_code, str_to_class(currency).objects.order_by("exc_date").last().value)
            for iso_code, currency in DESIRED_CURRENCIES.items()
        ]


def full_chart(request, currency):
    """
    Display a line chart containing all rates saved in the database.
    """

    c = str_to_class(currency).objects.values("exc_date", "value")

    iso_code = [
        iso_code
        for iso_code in DESIRED_CURRENCIES
        if DESIRED_CURRENCIES[iso_code] == currency.capitalize()
    ].pop()

    # Highcharts uses a list of lists, with inner lists having date in timestamp (milliseconds) and value.
    # The list have to be sorted by timestamp.
    rates = [[item["exc_date"].timestamp() * 1000, item["value"]] for item in c]
    sorted_rates = sorted(rates, key=lambda rate: rate[0])
    context = {
        "iso_code": iso_code,
        "currency": currency,
        "rates": sorted_rates,
    }

    return render(request, "exchange/chart.html", context)


def time_chart(request, currency):
    """
    Display a line chart containing rates between dates input by the user.
    """

    try:
        starting_date = datetime.strptime(request.POST["starting-date"], "%Y-%m-%d")
    except ValueError:
        starting_date = None
    try:
        ending_date = datetime.strptime(request.POST["ending-date"], "%Y-%m-%d")
    except ValueError:
        if starting_date is not None:
            ending_date = starting_date
        else:
            ending_date = None

    if (
        starting_date is not None
        and ending_date is not None
        and starting_date > ending_date
    ):
        starting_date, ending_date = ending_date, starting_date

    iso_code = [
        iso_code
        for iso_code in DESIRED_CURRENCIES
        if DESIRED_CURRENCIES[iso_code] == currency.capitalize()
    ].pop()

    context = get_rates(base="USD", date_start=starting_date, date_stop=ending_date)
    if context:
        context["currency"] = currency
        return render(request, "exchange/chart.html", context)

    c = (
        str_to_class(currency)
        .objects.filter(
            exc_date__range=[starting_date.isoformat(), ending_date.isoformat()]
        )
        .values("exc_date", "value")
    )
    if not c:
        context["currency"] = currency
        context["error"] = f"There are no {currency.capitalize()} rates to display."
        return render(request, "exchange/chart.html", context)

    # Highcharts uses a list of lists, with inner lists having date in timestamp (milliseconds) and value.
    # The list have to be sorted by timestamp.
    rates = [[item["exc_date"].timestamp() * 1000, item["value"]] for item in c]
    sorted_rates = sorted(rates, key=lambda rate: rate[0])
    context = {
        "iso_code": iso_code,
        "currency": currency,
        "rates": sorted_rates,
    }
    return render(request, "exchange/chart.html", context)
