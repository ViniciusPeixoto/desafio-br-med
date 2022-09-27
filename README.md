# BR Med Exchange Rate
This project is a Django Web Application that displays exchange rates for Europe's Euro (EUR), Brazil's Real (BRL) and Japan's Yen (JPY), all against USA's Dollar (USD). It works by collecting exchante rates data from [VAT Comply's Exchange Rate API](https://www.vatcomply.com/documentation#rates). Every time a rate is retrieved, the application stores it on a database. The user can choose to see a chart containing all rates already stored, or select a range of up to 5 business days and plot it.

## Application
The application is available online for a limited time. It was deployed using [DigitalOcean](https://www.digitalocean.com).
If you want to check it out, follow the link:
[BR Med Exchange Rate](https://br-med-exchangerate-nmmkz.ondigitalocean.app/)

### Pages
The application has 2 important web pages:
1. The main page
2. The chart page
On the main page, the user sees the application's name and a table with the latest rates for all three currencies. It also have a dropdown menu at the top of the page to access the charts containing all rates stored on the database.  
On the chart page, the user sees a chart with either all rates stored on the database or with a range of up to 5 business days they selected previously. The page also has two date pickers to give the user the ability to select a range of days, from a "starting date" to a "ending date". This selection have some limitations:
- The "starting date" cannot be empty
- The "starting date" cannot be in the future
- If the ending date is in the future, it defaults to "today"
- The difference between "starting date" and "ending date" cannot be above 5 business days
- A date cannot be before Jan 4th 1999

### Setup instructions for local development
If you wish to run the application locally, and improve on it, follow these instructions:
1. Clone this repository
```bash
> git clone https://github.com/ViniciusPeixoto/desafio-br-med.git
```
2. Move into the folder
```bash
> cd desafio-br-med/myexchangerate
```
3. Install the dependencies
```bash
> python -m pip install -r requirements.txt
```
4. Start the application
```bash
> python manage.py runserver
```

The application will be available at **http://127.0.0.1:8000/**.