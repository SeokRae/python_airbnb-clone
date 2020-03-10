from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):

    help = "This command creates RoomType"

    def handle(self, *args, **options):
        roomType = [
            "Entire place",
            "Private room",
            "Hotel room",
            "Shared room",
        ]
        for r in roomType:
            RoomType.objects.create(name=r)
        self.stdout.write(self.style.SUCCESS(f"{len(roomType)} RoomType created!"))
