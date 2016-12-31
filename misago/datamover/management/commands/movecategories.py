from ... import categories
from ..base import BaseCommand


class Command(BaseCommand):
    help = "Moves categories and labels from Misago 0.5 installation"

    def handle(self, *args, **options):
        self.stdout.write("Moving users from Misago 0.5:")

        self.start_timer()
        # categories.move_categories(self.stdout, self.style)
        self.stdout.write(
            self.style.SUCCESS("Moved categories in %s" % self.stop_timer()))

        self.start_timer()
        categories.move_labels()
        self.stdout.write(
            self.style.SUCCESS("Moved labels in %s" % self.stop_timer()))
