from django.core.management.base import BaseCommand
import random


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        for i in range(0, 10):
            if i % 2 == 0:
                print(random.randint(0, 15))
