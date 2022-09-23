from django.shortcuts import redirect


# Redirects the empty url to the exchange app's home page.
def home(request):
    return redirect('exchange:home')
