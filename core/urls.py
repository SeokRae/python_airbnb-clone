from django.urls import path

# core에서 app의 urls 관리
from rooms import views as room_views

app_name = "core"

urlpatterns = [
    path("", room_views.all_rooms, name="home"),
]
