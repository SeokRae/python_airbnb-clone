from django.core.management.base import BaseCommand
from users.models import User


# Seed로 만들어진 데이터의 avatar 값은 사용할 수 없는 데이터로 삭제 처리
class Command(BaseCommand):
    help = "This Command Delete Users Photos !"

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            user.avatar.delete(save=True)
            self.stdout.write(self.style.SUCCESS(f"{user.username} avatar deleted"))
