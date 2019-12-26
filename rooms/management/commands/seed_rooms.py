from django.core.management.base import BaseCommand
from django_seed import Seed

# Domain Models
from users import models as user_models
from rooms import models as room_models

import random


class Command(BaseCommand):

    help = "This command creates many Rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help="How many rooms do you want to create",
        )

    def handle(self, *args, **options):

        number = options.get("number")

        all_users = user_models.User.objects.filter(superhost=True)
        all_roomtype = room_models.RoomType.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(all_roomtype),
                "price": lambda x: random.randint(1, 300),
                "guests": lambda x: random.randint(1, 19),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} Rooms created Success !"))
