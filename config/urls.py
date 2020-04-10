"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# static 파일 제공 모듈
from django.conf.urls.static import static

# Server Error check Trigger
def trigger_error(request):
    division_by_zero = 1 / 0


# core에서 app의 urls 관리할 수 있도록 core.urls 추가
urlpatterns = [
    # main home page url mapping
    path("", include("core.urls", namespace="core")),
    # room category url mapping
    path("rooms/", include("rooms.urls", namespace="rooms")),
    # user category url mapping
    path("users/", include("users.urls", namespace="users")),
    # reservation category url mapping
    path("reservations/", include("reservations.urls", namespace="reservations")),
    # review category url mapping
    path("reviews/", include("reviews.urls", namespace="reviews")),
    # favorite room list category url mapping
    path("lists/", include("lists.urls", namespace="lists")),
    # conversation between users category url mapping
    path("conversations/", include("conversations.urls", namespace="conversations")),
    # admin page category url mapping
    path(os.environ.get("DJANGO_ADMIN"), admin.site.urls),
    # error check url mapping
    path("sentry-debug/", trigger_error),
]

# 개발 모드 or 프로덕션 모드인지 체크하여 URL Mapping
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
