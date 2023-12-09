from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from airport.forms import (PassengerCreateForm,
                           ReservationCreateForm,
                           ReservationUpdateForm,
                           AirportSearchForm,
                           FlightSearchForm,
                           AircraftSearchForm,
                           PassengerUpdateForm)
from airport.models import (Airline,
                            Aircraft,
                            Airport,
                            Passenger,
                            Reservation,
                            Flight)


@login_required
def index(request):
    num_airlines = Airline.objects.count()
    num_aircraft = Aircraft.objects.count()
    num_airports = Airport.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_airlines": num_airlines,
        "num_aircraft": num_aircraft,
        "num_airports": num_airports,
        "num_visits": num_visits + 1,
    }

    return render(request, "airport/index.html", context=context)


class PassengerCreateView(generic.CreateView):
    model = Passenger
    form_class = PassengerCreateForm
    success_url = "/"


class PassengerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Passenger


class PassengerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Passenger
    form_class = PassengerUpdateForm

    def get_success_url(self):
        return reverse(
            "airport:passenger-detail",
            kwargs={"pk": self.request.user.id}
        )


class ReservationCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ReservationCreateForm
    success_url = reverse_lazy("airport:index")
    template_name = "airport/reservation_form.html"

    def form_valid(self, form):
        reservation_instance = form.save(commit=False)
        reservation_instance.passenger = Passenger.objects.get(
            id=self.request.user.id
        )
        reservation_instance.save()
        return super().form_valid(form)


class ReservationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Reservation


class ReservationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Reservation
    form_class = ReservationUpdateForm

    def get_success_url(self):
        return reverse("airport:passenger-detail",
                       kwargs={"pk": self.request.user.id})


class ReservationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Reservation

    def get_success_url(self):
        return reverse("airport:passenger-detail",
                       kwargs={"pk": self.request.user.id})


class AirportListView(LoginRequiredMixin, generic.ListView):
    model = Airport
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AirportListView, self).get_context_data(**kwargs)
        city = self.request.GET.get("city", "")
        context["search_form"] = AirportSearchForm(
            initial={"city": city}
        )
        return context

    def get_queryset(self):
        queryset = Airport.objects.all()
        form = AirportSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                city__icontains=form.cleaned_data["city"]
            )
        return queryset


class FlightListView(LoginRequiredMixin, generic.ListView):
    model = Flight
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FlightListView, self).get_context_data(**kwargs)
        origin = self.request.GET.get("origin", "")
        destination = self.request.GET.get("destination", "")
        context["search_form"] = FlightSearchForm(
            initial={"origin": origin, "destination": destination}
        )
        return context

    def get_queryset(self):
        queryset = Flight.objects.all()
        form = FlightSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                origin__city__icontains=form.cleaned_data["origin"],
                destination__city__icontains=form.cleaned_data["destination"])
        return queryset


class AircraftListView(LoginRequiredMixin, generic.ListView):
    model = Aircraft
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AircraftListView, self).get_context_data(**kwargs)
        type = self.request.GET.get("type", "")
        context["search_form"] = AircraftSearchForm(
            initial={"type": type}
        )
        return context

    def get_queryset(self):
        queryset = Aircraft.objects.all()
        form = AircraftSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                type__icontains=form.cleaned_data["type"]
            )
        return queryset


class AircraftDetailView(LoginRequiredMixin, generic.DetailView):
    model = Aircraft
