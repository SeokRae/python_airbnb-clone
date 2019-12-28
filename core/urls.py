from django.urls import path
from rooms import views as room_views

app_name = "core"

# https://docs.djangoproject.com/en/2.2/topics/http/urls/
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
