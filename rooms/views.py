from django.views.generic import ListView
from . import models

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

    # Views에서 template으로 넘겨지는 object는 object_list, page_obj
