from django.core.management.base import BaseCommand
from users.models import User

NAME = "superuser"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="seok")
        if not admin:
            User.objects.create_superuser("seok", "seok@gmail.com", "1234")
            self.stdout.write(self.style.SUCCESS(f"{NAME} Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"{NAME} Exists"))
