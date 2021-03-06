import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from lists import models as list_models

NAME = "lists"


class Command(BaseCommand):

    help = f"This Command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):

        number = options.get("number")
        seeder = Seed.seeder()

        # Review의 상위 objects 선언
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        # seed entity 추가
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users)}
        )

        created_list = seeder.execute()
        clean_list = flatten(created_list.values())

        for pk in clean_list:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            # to_add는 QuerySet, *to_add는 QuerySet을 List로 풀어준다고 함
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
