from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from airport.models import Airline, Aircraft, Airport


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
