from django.views.generic import ListView, DetailView
from django_countries import countries
from django.shortcuts import render
from . import models

# Create your views here.


# class-based view인 ListView를 사용
class HomeView(ListView):

    """ HomeView Definition """

    # * 필수 설정인 model 설정
    model = models.Room

    # pagination option 설정
    paginate_by = 10
    paginate_orphans = 3
    ordering = "created"

    context_object_name = "rooms"
    # Views에서 template으로 넘겨지는 object는 object_list, page_obj

    class Meta:
        ordering = ["-id"]


# DetailView는 기본적으로 url argument로 pk를 찾는다.
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


# function-based search view
def search(request):
    print(request.GET.dict())
    # ?city= 가 빈 값이면 모르겠는데
    # queryString이 없을 경우 예외처리하고 /search/ 경로로 이동
    city = request.GET.get("city", "anywhere")
    city = str.capitalize(city)
    # country 설정 default 값 KR
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    # cast String to bool
    # on -> True로 변경됨
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    s_house_rules = request.GET.getlist("house_rules")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "s_house_rules": s_house_rules,
        "instant": instant,
        "superhost": superhost,
    }

    # DB Many-To-Many 값
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    room_types = models.RoomType.objects.all()
    house_rules = models.HouseRule.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    filter_args = {}
    # city filter
    if city != "Anywhere":
        filter_args["city__startswith"] = city

    # country filter
    filter_args["country"] = country

    # room type filter
    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)
    # pointer?
    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
