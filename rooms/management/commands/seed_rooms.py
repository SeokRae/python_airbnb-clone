import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

NAME = "rooms"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help=f"How many {NAME} you want to create"
        )

    # room 만들기
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        # room 객체의 restrict를 충족 시키기 위한 방법
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        seeder.add_entity(
            room_models.Room,  # Model
            number,  # digit
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
                "guests": lambda x: random.randint(0, 6),
            },
        )
        # room의 pk 값을 가져옴 해당 값은 dict(list(list())) 타입으로 되어 있음
        created_photos = seeder.execute()
        created_clean = flatten(created_photos.values())

        # number에 해당하는 room의 개수
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            # 랜덤한 photo 수 대입
            for i in range(3, random.randint(3, 14)):
                room_models.Photo.objects.create(
                    # caption에 해당하는 데이터를 sentence로 채움
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            # amenities 리스트 중에서 랜덤한 값을 room에 대입
            for a in amenities:
                magic_number = random.randint(0, amenities.count())
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            # facilities 리스트 중에서 랜덤한 값을 room에 대입
            for f in facilities:
                magic_number = random.randint(0, facilities.count())
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            # house_rule 리스트 중에서 랜덤한 값을 room에 대입
            for r in rules:
                magic_number = random.randint(0, rules.count())
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

            self.stdout.write(
                self.style.SUCCESS(f"{room.amenities.count()} apply amenities room!")
            )
            self.stdout.write(
                self.style.SUCCESS(f"{room.facilities.count()} apply facilities room!")
            )
            self.stdout.write(
                self.style.SUCCESS(f"{room.house_rules.count()} apply house_rule room!")
            )
            self.stdout.write(self.style.SUCCESS(f" * create {room.name} room"))
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
