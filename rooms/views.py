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
    # ?city= 가 빈 값이면 모르겠는데
    # queryString이 없을 경우 예외처리하고 /search/ 경로로 이동
    city = request.GET.get("city", "anywhere")
    city = str.capitalize(city)
    room_types = models.RoomType.objects.all()
    return render(
        request,
        "rooms/search.html",
        # template으로 넘겨줄 context (city, countries, room_types)
        {"city": city, "countries": countries, "room_types": room_types},
    )
