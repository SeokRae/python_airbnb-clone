from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from . import models

# Create your views here.


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()

    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(int(page))  # page(), get_page() 차이
        return render(request, "rooms/all_rooms.html", context={"page": rooms},)

    except ValueError:
        return redirect("/")

    except (EmptyPage, PageNotAnInteger):
        return redirect("/")
