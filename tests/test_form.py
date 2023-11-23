from django.contrib.auth import get_user_model
from django.test import TestCase

from airport.forms import PassengerCreateForm
from airport.models import Airport
from tests.test_view import AIRPORT_URL


class PassengerCreateFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "passenger1",
            "password1": "test_password123",
            "password2": "test_password123",
            "passport": "QW123456",
            "first_name": "Ivan",
            "last_name": "Ivanov"
        }

    def test_create_passenger_with_valid_passport(self):
        form = PassengerCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_create_passenger_with_invalid_passport_letters(self):
        self.form_data["passport"] = "Qw123456"
        form = PassengerCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)

    def test_create_passenger_with_invalid_passport_digits(self):
        self.form_data["passport"] = "QW123G54"
        form = PassengerCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)

    def test_create_passenger_with_invalid_passport_length(self):
        self.form_data["passport"] = "QWE1235"
        form = PassengerCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)

    def test_create_passenger_with_unmatched_passwords(self):
        self.form_data["password1"] = "test_password129"
        form = PassengerCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)


class SearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="pass12345"
        )
        self.client.force_login(self.user)

    def test_search_aircraft_by_type(self):
        manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        first_car = Car.objects.create(
            model="Grand Cherokee",
            manufacturer=manufacturer
        )
        second_car = Car.objects.create(
            model="Gladiator",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL, {"model": first_car})
        self.assertContains(response, first_car)
        self.assertNotContains(response, second_car)

    def test_search_driver_by_username(self):
        driver1 = Driver.objects.create(
            username="ivan",
            password="driver1pass",
            license_number="QWE12345"
        )
        driver2 = Driver.objects.create(
            username="vasiliy",
            password="driver2pass",
            license_number="QWE54321"
        )
        response = self.client.get(DRIVER_URL, {"username": driver1.username})
        self.assertContains(response, driver1.username)
        self.assertNotContains(response, driver2.username)

    def test_search_airport_by_city(self):
        airport1 = Airport.objects.create(
            icao_designator="UKBB",
            city="Boryspil"
        )
        airport2 = Airport.objects.create(
            icao_designator="UKKK",
            city="Kyiv"
        )
        response = self.client.get(
            AIRPORT_URL,
            {"city": airport1.city})
        self.assertContains(response, airport1.city)
        self.assertNotContains(response, airport2.city)
