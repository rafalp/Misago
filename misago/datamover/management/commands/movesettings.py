from misago.datamover.management.base import BaseCommand
from misago.datamover.settings import move_settings


class Command(BaseCommand):
    help = "Moves settings from Misago 0.5"

    def handle(self, *args, **options):
        self.stdout.write("Moving settings from Misago 0.5:")

        self.start_timer()
        move_settings(self.stdout)

        self.stdout.write(self.style.SUCCESS("Moved settings in %s" % self.stop_timer()))
