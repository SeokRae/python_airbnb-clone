from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "get_host",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)

    search_fields = ("^room__name",)

    raw_id_fields = (
        "room",
        "guest",
    )


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    list_display = ("day", "reservation")

    raw_id_fields = ("reservation",)
