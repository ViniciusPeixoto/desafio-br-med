from datetime import datetime
import json
import requests
import sys

from pandas import bdate_range

from .models import Euro, Real, Yen

# What currencies the app will support.
DESIRED_CURRENCIES = {
    'EUR': 'Euro',
    'BRL': 'Real',
    'JPY': 'Yen'
}
BASE_CURRENCY = 'USD'


def get_vat_rates(date: datetime, base=BASE_CURRENCY):
    """
    Make a GET request at VAT Comply's Exchange Rates API.
    """

    params = {'base': base, 'date': date.date().isoformat()}
    vat_rates = requests.get("https://api.vatcomply.com/rates", params=params)

    if vat_rates.status_code != 200:
        return {'error': "API request failed."}

    return json.loads(vat_rates.content.decode('utf-8'))


def time_slicing(date_start, date_stop=None, base=BASE_CURRENCY):
    """
    GETs Exchange Rates from VAT Comply's API from a range of maximum 5 business days.
    If 'date_stop' is None, then GETs a single rate.
    """

    vat_rates = []

    if date_start is None:
        return {'error': "Please, choose a starting date."}

    if date_stop is None or date_start == date_stop:
        vat_rates.append(get_vat_rates(base=base, date=date_start))
        return vat_rates

    if date_stop > datetime.today():
        date_stop = datetime.today()

    date_list = bdate_range(date_start, date_stop).to_list()
    if len(date_list) > 5:
        return {'error': "Dates are too far apart. Choose a narrower span."}

    for date in date_list:
        vat_rates.append(get_vat_rates(base=base, date=date))

    return vat_rates


def str_to_class(classname: str):
    """
    Return the class of given string.
    """

    return getattr(sys.modules[__name__], classname.capitalize())


def save_current_rates(desired_rates, rates_date):
    """
    Saves rates from a dict to the database if there is not already a rate for the given date.
    """

    for iso_code, value in desired_rates.items():
        c = str_to_class(DESIRED_CURRENCIES[iso_code]).objects.filter(exc_date=rates_date).last()
        if not c:
            c = str_to_class(DESIRED_CURRENCIES[iso_code])(exc_date=rates_date, value=value)
            c.save()


def get_rates(base, date_start, date_stop=None):
    """
    Makes requests for VAT Comply's Exchange Rate API and save these rates to the database.
    """

    list_vat_rates = time_slicing(date_start=date_start, date_stop=date_stop, base=base)

    for vat_rate in list_vat_rates:
        if 'error' in vat_rate:
            return list_vat_rates

        rates_date = vat_rate['date']
        desired_rates = {
            iso_code: "{:.3f}".format(vat_rate['rates'][iso_code]) for iso_code in DESIRED_CURRENCIES.keys()
        }
        save_current_rates(desired_rates, rates_date)

    return {}
