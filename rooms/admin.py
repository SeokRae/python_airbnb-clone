from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    # ManyToMany 필드에서 Room 객체 접근
    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


# room에 photo를 추가 하기 위한 inline
class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",  # def count_amenities function의 반환 값
        "count_photos",  # def count_photos function의 반환 값
        "total_rating",  # Model에 만든 def total_rating의 반환 값
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = ("=city", "^host__username")

    filter_horizontal = ("amenities", "facilities", "house_rules")

    # self는 RoomAdmin, obj는 현재 행(row)
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()
