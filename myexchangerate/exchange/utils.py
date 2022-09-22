import requests
import json
import sys

from .models import Euro, Real, Yen

DESIRED_CURRENCIES = {'EUR': 'Euro', 'BRL': 'Real', 'JPY': 'Yen'}


def get_vat_rates():
    vat_rates = requests.get("https://api.vatcomply.com/rates?base=USD")

    if vat_rates.status_code != 200:
        return {}

    return json.loads(vat_rates.content.decode('utf-8'))


def get_current_rates():
    dict_vat_rates = get_vat_rates()
    if not dict_vat_rates:
        return {}

    rates_date = dict_vat_rates['date']
    desired_rates = {
        currency: "{:.3f}".format(dict_vat_rates['rates'][currency]) for currency in DESIRED_CURRENCIES.keys()}

    save_current_rates(desired_rates, rates_date)
    return desired_rates.items()


def save_current_rates(desired_rates, rates_date):
    for iso_code, value in desired_rates.items():
        c = str_to_class(DESIRED_CURRENCIES[iso_code]).objects.filter(exc_date=rates_date).last()
        if not c:
            c = str_to_class(DESIRED_CURRENCIES[iso_code])(exc_date=rates_date, value=value)
            c.save()


def str_to_class(classname: str):
    return getattr(sys.modules[__name__], classname.capitalize())
