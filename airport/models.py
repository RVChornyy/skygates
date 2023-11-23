from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Airline(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Aircraft(models.Model):
    type = models.CharField(max_length=63)
    call_sign = models.CharField(max_length=6, unique=True)
    capacity = models.IntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="aircraft")

    class Meta:
        verbose_name = "aircraft"
        verbose_name_plural = "aircraft"

    def __str__(self):
        return self.type


class Airport(models.Model):
    icao_designator = models.CharField(max_length=4)
    city = models.CharField(max_length=63)

    class Meta:
        ordering = ["city"]

    def __str__(self):
        return f"{self.city} ({self.icao_designator})"


class Flight(models.Model):
    number = models.CharField(max_length=10, unique=True)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    aircraft = models.ManyToManyField(Aircraft, related_name="flights")

    def __str__(self):
        return f"{self.number} from {self.origin} to {self.destination}"


class Passenger(AbstractUser):
    passport = models.CharField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse("airport:passenger-detail", kwargs={"pk": self.pk})


class Reservation(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservations")
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="reservations")

    def __str__(self):
        return f"{self.flight}"
