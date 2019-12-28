# https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/
from django.views.generic import ListView
from django.utils import timezone
from . import models

# Create your views here.


class HomeView(ListView):

    """ HomeView class Definition """

    model = models.Room

    paginate_by = 10  # paging
    paginate_orphans = 2
    ordering = "created"

    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
