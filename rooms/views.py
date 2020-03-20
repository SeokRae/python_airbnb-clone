from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms

# Create your views here.


# class-based view인 ListView를 사용
class HomeView(ListView):

    """ HomeView Definition """

    # * 필수 설정인 model 설정
    model = models.Room

    # pagination option 설정
    paginate_by = 10
    paginate_orphans = 3
    ordering = "created"

    context_object_name = "rooms"
    # Views에서 template으로 넘겨지는 object는 object_list, page_obj

    class Meta:
        ordering = ["-id"]


# DetailView는 기본적으로 url argument로 pk를 찾는다.
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


# class-based View
class SearchView(View):
    """ SearchView Definition """

    # function-based search view
    def get(self, request):

        country = request.GET.get("country")

        if country:
            # bounded form > forms.SearchForm(request.GET)
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")  # QuerySet
                facilities = form.cleaned_data.get("facilities")  # QuerySet

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                for amenity in amenities:
                    qs = qs.filter(amenities=amenity)

                for facility in facilities:
                    qs = qs.filter(facilities=facility)

                paginator = Paginator(qs, 5, orphans=2)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms},
                )
        else:

            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})
