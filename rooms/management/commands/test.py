from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command tells me that he loves me"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that I love you?"
        )

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        times = options.get("times")
        for t in range(0, int(times)):
            self.stdout.write(self.style.SUCCESS("I love you"))
