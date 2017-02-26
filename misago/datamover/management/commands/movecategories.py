from misago.datamover import categories
from misago.datamover.management.base import BaseCommand


class Command(BaseCommand):
    help = "Moves categories and labels from Misago 0.5"

    def handle(self, *args, **options):
        self.stdout.write("Moving categories from Misago 0.5:")

        self.start_timer()
        categories.move_categories(self.stdout, self.style)
        self.stdout.write(self.style.SUCCESS("Moved categories in %s" % self.stop_timer()))

        self.start_timer()
        categories.move_labels()
        self.stdout.write(self.style.SUCCESS("Moved labels in %s" % self.stop_timer()))
