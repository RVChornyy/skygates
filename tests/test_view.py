from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from airport.models import Aircraft, Airline, Airport, Flight

AIRCRAFT_URL = reverse("airport:aircraft-list")
AIRPORT_URL = reverse("airport:airport-list")
FLIGHT_URL = reverse("airport:flight-list")


class PublicAircraftTest(TestCase):
    def test_login_required(self):
        response = self.client.get(AIRCRAFT_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateAircraftTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_aircraft(self):
        company = Airline.objects.create(
            name="test_company"
        )
        Aircraft.objects.create(
            type="Boeing 787",
            call_sign="QWE-124",
            capacity=300,
            airline=company
        )
        Aircraft.objects.create(
            type="Boeing 747",
            call_sign="QWE-123",
            capacity=300,
            airline=company
        )
        response = self.client.get(AIRCRAFT_URL)
        planes = Aircraft.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airport/aircraft_list.html")
        self.assertEqual(list(response.context["aircraft_list"]), list(planes))


class PublicAirportTest(TestCase):
    def test_login_required(self):
        response = self.client.get(AIRPORT_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateAirportTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_airports(self):
        Airport.objects.create(
            icao_designator="UKKK",
            city="Kyiv"
        )
        Airport.objects.create(
            icao_designator="UKBB",
            city="Boryspil"
        )
        response = self.client.get(AIRPORT_URL)
        airports = Airport.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airport/airport_list.html")
        self.assertEqual(
            list(response.context["airport_list"]), list(airports)
        )


class PublicFlightTest(TestCase):
    def test_login_required(self):
        response = self.client.get(FLIGHT_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateFlightTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_flights(self):
        company = Airline.objects.create(
            name="test_company"
        )
        airport = Airport.objects.create(
            icao_designator="UKKK",
            city="Kyiv"
        )
        plane = Aircraft.objects.create(
            type="Boeing 747",
            call_sign="QWE-123",
            capacity=300,
            airline=company
        )

        flight1 = Flight.objects.create(
            number="QQQ-000",
            origin=airport,
            destination=airport,
            airline=company,
        )
        flight1.aircraft.add(plane)
        flight2 = Flight.objects.create(
            number="QQQ-001",
            origin=airport,
            destination=airport,
            airline=company,
        )
        flight2.aircraft.add(plane)
        response = self.client.get(FLIGHT_URL)
        flights = Flight.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airport/flight_list.html")
        self.assertEqual(list(response.context["flight_list"]), list(flights))
