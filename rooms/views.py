from django.shortcuts import render
from . import models

# Create your views here.


def all_rooms(request):
    page = int(request.GET.get("page", 1))
    page_size = 10

    limit = page * page_size
    offset = limit - page_size

    all_rooms = models.Room.objects.all()[offset:limit]
    return render(request, "rooms/all_rooms.html", context={"rooms": all_rooms})
