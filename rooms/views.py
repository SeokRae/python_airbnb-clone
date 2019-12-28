# https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/
from django.views.generic import ListView
from . import models

# Create your views here.


class HomeView(ListView):

    """ HomeView class Definition """

    model = models.Room

    paginate_by = 10  # paging
    paginate_orphans = 2
    ordering = "created"

    pass
