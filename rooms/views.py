# https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models

# Create your views here.


class HomeView(ListView):

    """ HomeView class Definition """

    model = models.Room

    paginate_by = 10  # paging
    paginate_orphans = 2
    ordering = "created"

    context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail class Definition """

    model = models.Room


# Function Base View
def search(request):
    # Request Parameter
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")

    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))

    s_amenities = request.GET.get("amenities")
    s_facilities = request.GET.get("facilities")

    # Page Data
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(request, "rooms/search.html", {**form, **choices},)
