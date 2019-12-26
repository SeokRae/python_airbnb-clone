from django.core.management.base import BaseCommand
from django_seed import Seed

# Domain Models
from users import models as user_models
from rooms import models as room_models
from reviews import models as review_models
import random


class Command(BaseCommand):

    help = "This command creates many Reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help="How many reviews do you want to create",
        )

    def handle(self, *args, **options):

        number = options.get("number")

        all_users = user_models.User.objects.filter(superhost=False)
        all_rooms = room_models.Room.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "value": lambda x: random.randint(0, 5),
                "accuracy": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "check_in": lambda x: random.randint(0, 5),
                "cleanliness": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "user": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Reviews created Success !"))
