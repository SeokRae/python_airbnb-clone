from django.core.management.base import BaseCommand
from rooms.models import HouseRule

NAME = "House Rules"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        house_rules = [
            "Suitable for events",
            "Pets allowed",
            "Smoking allowed",
        ]
        for r in house_rules:
            HouseRule.objects.create(name=r)

        self.stdout.write(self.style.SUCCESS(f"{len(house_rules)} {NAME} created!"))
