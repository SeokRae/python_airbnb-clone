from django.core.management.base import BaseCommand
from rooms.models import RoomType

NAME = "RoomType"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        roomType = [
            "Entire place",
            "Private room",
            "Hotel room",
            "Shared room",
        ]
        for r in roomType:
            RoomType.objects.create(name=r)
        self.stdout.write(self.style.SUCCESS(f"{len(roomType)} {NAME} created!"))
