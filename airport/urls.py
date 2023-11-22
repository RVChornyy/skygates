from django.urls import path

from airport.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "airport"
