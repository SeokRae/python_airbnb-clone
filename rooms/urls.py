from django.urls import path
from . import views

app_name = "rooms"

# def _path(route, view, kwargs=None, name=None, Pattern=None):
urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/edit/photos/", views.EditRoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/edit/photos/add", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:room_pk>/edit/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/edit/photos/<int:photo_pk>/edit/",
        views.EditRoomPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
