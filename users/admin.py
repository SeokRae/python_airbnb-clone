from django.contrib import admin

# admin write page custom
from django.contrib.auth.admin import UserAdmin

# admin.py 파일과 동일한 폴더 내에 models를 호출 (User.class)
from . import models

# room model 가져오기 위함
from rooms.models import Room


# User에 Room을 추가 하기 위한 inline
class RoomInline(admin.StackedInline):

    model = Room


# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "email_secret",
                    "email_verified",
                    "login_method",
                )
            },
        ),
    )

    # 기본 필터에 superhost 확인
    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )
