from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from . import utils


class UtilsTests(TestCase):
    def test_get_vat_rates_before_jan_4_1999(self):
        """
        get_vat_rates() should fail to get rates before Jan 4th 1999.
        """

        date = datetime.strptime("1999-01-03", "%Y-%m-%d")
        request_result = utils.get_vat_rates(date=date)
        expected_result = {"error": "API request failed."}

        self.assertDictEqual(request_result, expected_result)

    def test_get_vat_rates_in_the_future(self):
        """
        get_vat_rates() should return the latest rates if the date of the request is later than the latest available.
        """

        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        request_result = utils.get_vat_rates(date=tomorrow)
        expect_result = utils.get_vat_rates(date=today)

        self.assertEqual(request_result, expect_result)

    def test_time_slicing_no_date_start(self):
        """
        time_slicing() should return an error if no starting date is choosen by the user.
        """

        date_start = None
        request_result = utils.time_slicing(date_start=date_start)
        expected_result = {"error": "Please, choose a starting date."}

        self.assertEqual(request_result, expected_result)

    def test_time_slicing_no_date_stop(self):
        """
        time_slicing() should make ONE get_vat_rates() for the starting date.
        """

        date_start = datetime.today()
        request_result = utils.time_slicing(date_start=date_start, date_stop=None)
        expected_result = [utils.get_vat_rates(date=date_start)]

        self.assertEqual(request_result, expected_result)

    def test_time_slicing_range_above_5_business_days(self):
        """
        time_slicing() should check for time range above 5 business days and return an error.
        """

        date_start = datetime.today() - timedelta(days=9)
        date_stop = datetime.today()
        request_result = utils.time_slicing(date_start=date_start, date_stop=date_stop)
        expected_result = {"error": "Dates are too far apart. Choose a narrower span."}

        self.assertEqual(request_result, expected_result)

    def test_time_slicing_future_dates(self):
        """
        time_slicing() should treat future dates as the latest day available.
        """

        yesterday = datetime.today() - timedelta(days=1)
        the_day_after_tomorrow = datetime.today() + timedelta(days=2)
        request_result = utils.time_slicing(
            date_start=yesterday, date_stop=the_day_after_tomorrow
        )
        expected_result = utils.time_slicing(
            date_start=yesterday, date_stop=datetime.today()
        )

        self.assertEqual(request_result, expected_result)

    def test_slicing_reversed_dates(self):
        """
        time_slicing() should work even if date_stop < date_start.
        """

        the_day_before_yesterday = datetime.today() - timedelta(days=2)
        today = datetime.today()
        request_result = utils.time_slicing(
            date_start=today, date_stop=the_day_before_yesterday
        )
        expected_result = utils.time_slicing(
            date_start=the_day_before_yesterday, date_stop=today
        )

        self.assertEqual(request_result, expected_result)

    def test_slicing_same_dates(self):
        """
        time_slicing() should treat date_start == date_stop as one date.
        """
        today = datetime.today()
        request_result = utils.time_slicing(date_start=today, date_stop=today)
        expected_result = utils.time_slicing(date_start=today)

        self.assertEqual(request_result, expected_result)


class HomeViewTests(TestCase):
    client = Client()

    def test_home_view(self):
        page_response = self.client.get(reverse("exchange:home"))

        self.assertEqual(page_response.status_code, 200)
        self.assertContains(page_response, "EUR")
        self.assertContains(page_response, "Full EUR Rates")
        self.assertContains(page_response, "BRL")
        self.assertContains(page_response, "Full BRL Rates")
        self.assertContains(page_response, "JPY")
        self.assertContains(page_response, "Full JPY Rates")
