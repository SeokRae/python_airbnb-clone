from django.contrib import admin

# admin.py 파일과 동일한 폴더 내에 models를 호출 (User.class)
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
