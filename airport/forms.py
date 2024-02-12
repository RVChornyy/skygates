from django.contrib.auth.forms import UserCreationForm
from django import forms
from airport.models import Passenger, Reservation
from airport.service.validations import validate_passport


class PassengerCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Passenger
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "passport"
        )

    def clean_passport(self):
        return validate_passport(self.cleaned_data["passport"])


class PassengerUpdateForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ["username",
                  "first_name",
                  "last_name",
                  "passport"]

    def clean_passport(self):
        return validate_passport(self.cleaned_data["passport"])


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("flight",)


class ReservationUpdateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("flight",)


class AirportSearchForm(forms.Form):
    city = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by city",
                "style": "width: 250px"
            }
        )
    )


class FlightSearchForm(forms.Form):
    origin = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by departure",
                "style": "width:250px"
            }
        )
    )
    destination = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by arrival",
                "style": "width: 250px"
            }
        )
    )


class AircraftSearchForm(forms.Form):
    type = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by type",
                "style": "width: 250px"
            }
        )
    )
