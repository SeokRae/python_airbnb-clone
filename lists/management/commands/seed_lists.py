from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

# Domain Models
from users import models as user_models
from rooms import models as room_models
from lists import models as list_models
import random

NAME = "Lists"


class Command(BaseCommand):

    help = f"This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help=f"How many {NAME} do you want to create",
        )

    def handle(self, *args, **options):

        number = options.get("number")

        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(all_users)},
        )
        created_lists = seeder.execute()
        lists_pks = flatten(list(created_lists.values()))

        for pk in lists_pks:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = all_rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created Success !"))
