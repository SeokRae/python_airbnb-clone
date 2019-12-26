from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
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
        all_amenities = room_models.Amenity.objects.all()
        all_facilities = room_models.Facility.objects.all()
        all_rules = room_models.HouseRule.objects.all()

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
        created_rooms = seeder.execute()
        rooms_pks = flatten(list(created_rooms.values()))

        # put the photo in series of rooms
        for pk in rooms_pks:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(random.randint(3, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )

            for a in all_amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in all_facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in all_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} Rooms created Success !"))
