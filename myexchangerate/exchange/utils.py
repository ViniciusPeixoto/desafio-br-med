import json
import requests
import sys
import pandas as pd

from .models import Euro, Real, Yen

DESIRED_CURRENCIES = {'EUR': 'Euro', 'BRL': 'Real', 'JPY': 'Yen'}


def get_vat_rates(base: str, date: str):
    params = {'base': base, 'date': date}
    vat_rates = requests.get("https://api.vatcomply.com/rates", params=params)

    if vat_rates.status_code != 200:
        return {'error': "API request failed."}

    return json.loads(vat_rates.content.decode('utf-8'))


def get_rates(base, date_start, date_stop=None):
    list_vat_rates = time_slicing(base, date_start, date_stop)
    for rate in list_vat_rates:
        if rate.get('error'):
            return rate

    for vat_rate in list_vat_rates:
        rates_date = vat_rate['date']
        desired_rates = {
            iso_code: "{:.3f}".format(vat_rate['rates'][iso_code]) for iso_code in DESIRED_CURRENCIES.keys()}
        save_current_rates(desired_rates, rates_date)

    return {}


def save_current_rates(desired_rates, rates_date):
    for iso_code, value in desired_rates.items():
        c = str_to_class(DESIRED_CURRENCIES[iso_code]).objects.filter(exc_date=rates_date).last()
        if not c:
            c = str_to_class(DESIRED_CURRENCIES[iso_code])(exc_date=rates_date, value=value)
            c.save()


def str_to_class(classname: str):
    return getattr(sys.modules[__name__], classname.capitalize())


def time_slicing(base, date_start, date_stop):
    vat_rates = []
    if date_stop is None:
        vat_rates.append(get_vat_rates(base, date_start.date().isoformat()))
        return vat_rates

    date_list = pd.bdate_range(date_start, date_stop).to_list()
    if len(date_list) > 5:
        return {'error': "Dates are too far apart. Choose a narrower span"}

    for date in date_list:
        vat_rates.append(get_vat_rates(base, date.date().isoformat()))

    return vat_rates
