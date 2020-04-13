import random
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as revservation_models
from rooms import models as room_models
from users import models as user_models
from reservations import models as reservation_models

NAME = "reservations"


class Command(BaseCommand):

    help = f"This Command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):

        number = options.get("number")
        seeder = Seed.seeder()

        # Review의 상위 objects 선언
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        # seed entity 추가
        seeder.add_entity(
            revservation_models.Reservation,
            number,
            {
                # list방식의 choice도 가능
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                # dateTime방식 만들기
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(2, 6)),
            },
        )

        created_reservation = seeder.execute()
        clean_reservations = flatten(created_reservation.values())

        # reservation 생성시 check_in ~ check_out 기간 내에 bookedday 만들기
        for pk in clean_reservations:
            reservation = revservation_models.Reservation.objects.get_or_none(pk=pk)
            start = reservation.check_in
            end = reservation.check_out
            diff = end - start

            # reservation의 check_in ~ check_out의 range를 없으면 생성
            for i in range(diff.days + 1):
                day = start + timedelta(days=i)

                bookedday = reservation_models.BookedDay.objects.create(
                    reservation=reservation, day=day
                )
                self.stdout.write(self.style.SUCCESS(f"{bookedday} booked_day created"))

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
