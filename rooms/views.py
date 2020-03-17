from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import models

# Create your views here.


def all_rooms(request):
    page = request.GET.get("page", 1)
    # 
    room_list = models.Room.objects.get_queryset().order_by("id")
    # Paginator(object_list, per_page, orphans=0, allow_empty_first_page=True)
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        # 잘못된 페이지 번호 처리
        pages = paginator.page(page)
        return render(request, "rooms/home.html", {"pages": pages},)
    except EmptyPage:  # 페이지 범위 외의 값 입력시 예외처리
        return redirect("/")
    except PageNotAnInteger:  # page 파라미터의 값이 Integer가 아닐 경우 예외처리
        return redirect("/")
