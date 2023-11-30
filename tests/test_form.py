from django.contrib.auth import get_user_model
from django.test import TestCase

from airport.forms import PassengerCreateForm
from airport.models import Airport, Airline, Aircraft, Flight
from tests.test_view import AIRPORT_URL, AIRCRAFT_URL, FLIGHT_URL


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
        company = Airline.objects.create(
            name="test_company"
        )
        plane1 = Aircraft.objects.create(
            type="Boeing 787",
            call_sign="QWE-124",
            capacity=300,
            airline=company
        )
        plane2 = Aircraft.objects.create(
            type="Boeing 747",
            call_sign="QWE-123",
            capacity=300,
            airline=company
        )
        response = self.client.get(AIRCRAFT_URL, {"type": plane1})
        self.assertContains(response, plane1)
        self.assertNotContains(response, plane2)

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

    def test_search_flight_by_destination(self):
        company = Airline.objects.create(
            name="test_company"
        )
        airport1 = Airport.objects.create(
            icao_designator="UKKK",
            city="Kyiv"
        )
        airport2 = Airport.objects.create(
            icao_designator="UKHH",
            city="Kharkiv")
        airplane = Aircraft.objects.create(
            type="Boeing 747",
            call_sign="QWE-123",
            capacity=300,
            airline=company
        )

        flight1 = Flight.objects.create(
            number="QQQ-000",
            origin=airport1,
            destination=airport1,
            airline=company,
        )
        flight1.aircraft.add(airplane)
        flight2 = Flight.objects.create(
            number="QQQ-001",
            origin=airport2,
            destination=airport2,
            airline=company,
        )
        flight2.aircraft.add(airplane)
        response = self.client.get(
            FLIGHT_URL,
            {"destination": flight1.destination})
        self.assertContains(response, flight1.destination)
        self.assertNotContains(response, flight2.destination)
