# Airbnb Clone

## 1 Environment Setup

## 2 Introduction to Django

## 3 User App

## 4 Room App

## 5 All Other Apps!

## 6 Room Admin

## 7 Models and QuerySets

## 8 More Admins!

## 9 Custom Commands and Seeding

## 10 Introduction to Views and Urls

## 11 HomeView

 - python으로 구현하는 paging
```
    def all_rooms(request):
    
        page = request.GET.get("page", 1)
        page = int(page or 1)
        
        page_size = 10
        limit = page_size * page
        offset = limit - page_size
        
        all_rooms = models.Room.objects.all()[offset:limit]
        page_count = ceil(models.Room.objects.count() / page_size)

        return render(
            request,
            "rooms/home.html",
            {
                "potato": all_rooms,
                "page": page,
                "page_count": page_count,
                "page_range": range(1, page_count),
            },
        )
```

```
    {% for page in page_range %}
        <a href="?page={{page}}">{{page}}</a>
    {% endfor %}
```

 - view 수정
```
    {% if page is not 1 %}
        <a href="?page={{page|add:-1}}">Previous</a>
    {% endif %}

    Page {{page}} of {{page_count}}

    {% if not page == page_count  %}
        <a href="?page={{page|add:1}}">Next</a>
    {% endif %}
```

 - paginator를 이용한 paging
```
from django.core.paginator import Paginator
...

    def all_rooms(request):
        page = request.GET.get("page")
        room_list = models.Room.objects.all()
        paginator = Paginator(room_list, 10)
        rooms = paginator.get_page(page)
        return render(request, "rooms/home.html", {"rooms": rooms})
```

```
    {% for room in rooms.object_list  %}
        <h1>{{room.name}} / ${{room.price}}</h1>
    {% endfor %}

    {% if rooms.has_previous %}
        <a href="?page={{rooms.number|add:-1}}">Previous</a>
    {% endif %}
    Page {{rooms.number}} of {{rooms.paginator.num_pages}}
    {% if rooms.has_next  %}
        <a href="?page={{rooms.number|add:1}}">Next</a>
    {% endif %}
```

 - get_page vs page
```
    def all_rooms(request):
        page = request.GET.get("page", 1)
        room_list = models.Room.objects.all()
        paginator = Paginator(room_list, 10, orphans=5)
        rooms = paginator.page(int(page))

        return render(request, "rooms/home.html", {"page": rooms})
```

```
    {% for room in page.object_list  %}
        <h1>{{room.name}} / ${{room.price}}</h1>
    {% endfor %}

    {% if page.has_previous %}
        <a href="?page={{page.previous_page_number}}">Previous</a>
    {% endif %}

    Page {{page.number}} of {{page.paginator.num_pages}}
    
    {% if page.has_next  %}
        <a href="?page={{page.next_page_number}}">Next</a>
    {% endif %}
```

 - paging Handling Exception
```
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage

def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")
```

 - ListView 사용

```{python}
# core/urls.py
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
```

```{python}
from django.views.generic import ListView

class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
```
## 12 DetailView

## 13 SearchView

## 14 User Log in & Log out

## 15 Sign Up 

## 16 Verify Email

## 17 Log in with Github

## 18 Kakao Login

## 19 Intro to TailwindCSS

## 20 Make it all BEAUTIFUL

## 21 User Profile, Edit Profile, Change Password

## 22 Room Detail

## 23 Update Room, Create Room, Room Photos

## 24 Reservations and Reviews

## 25 Translations, Lists and Messages
