from django.shortcuts import render
from django.core.paginator import Paginator

from . import models

# Create your views here.


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    # Paginator(object_list, per_page, orphans=0, allow_empty_first_page=True)
    paginator = Paginator(room_list, 10)
    # 잘못된 페이지 번호 처리
    rooms = paginator.get_page(page)
    print(rooms.paginator.num_pages)
    return render(request, "rooms/home.html", {"rooms": rooms},)
