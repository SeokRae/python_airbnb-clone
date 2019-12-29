from django.urls import path
from . import views

app_name = "rooms"

# https://github.com/SeokRae/python_airbnb-clone/issues/4
urlpatterns = [path("<int:pk>", views.HomeView.room_detail, name="detail")]
