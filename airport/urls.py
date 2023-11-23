from django.urls import path

from airport.views import index, PassengerCreateView, PassengerDetailView, \
    ReservationCreateView, ReservationDetailView, ReservationUpdateView, ReservationDeleteView, AirportListView, \
    FlightListView, AircraftListView, AircraftDetailView, PassengerUpdateView

urlpatterns = [
    path("", index, name="index"),
    path("passengers/create/", PassengerCreateView.as_view(), name="passenger-create"),
    path("passengers/<int:pk>/", PassengerDetailView.as_view(), name="passenger-detail"),
    path("passengers/<int:pk>/update/", PassengerUpdateView.as_view(), name="passenger-update"),
    path("reservations/create/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reservations/<int:pk>/", ReservationDetailView.as_view(), name="reservation-detail"),
    path("reservations/<int:pk>/update/", ReservationUpdateView.as_view(), name="reservation-update"),
    path("reservations/<int:pk>/delete/", ReservationDeleteView.as_view(), name="reservation-delete"),
    path("airports/", AirportListView.as_view(), name="airport-list"),
    path("flights/", FlightListView.as_view(), name="flight-list"),
    path("aircraft/", AircraftListView.as_view(), name="aircraft-list"),
    path("aircraft/<int:pk>/", AircraftDetailView.as_view(), name="aircraft-detail"),
]

app_name = "airport"
