from django.urls import path
from . import views

app_name = "rooms"

# def _path(route, view, kwargs=None, name=None, Pattern=None):
urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.search, name="search"),
]