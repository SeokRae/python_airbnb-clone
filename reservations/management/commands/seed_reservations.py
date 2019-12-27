from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django_seed import Seed

# Domain Models
from users import models as user_models
from rooms import models as room_models
from reservations import models as reservation_models
import random

NAME = "Reservations"


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

        all_rooms = room_models.Room.objects.all()
        all_guests = user_models.User.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "check_in": lambda x: datetime.now()
                - timedelta(days=random.randint(-2, 2)),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
                "guest": lambda x: random.choice(all_guests),
                "room": lambda x: random.choice(all_rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created Success !"))
