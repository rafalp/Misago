from django.core.management.base import BaseCommand, CommandError

from ...models import PostSnapshot


class Command(BaseCommand):
    help = "Deletes all post snapshots"

    def handle(self, *args, **options):
        snapshots = PostSnapshot.objects.count()

        if not snapshots:
            self.stdout.write("No snapshots exist")
            return

        if input(f"Type 'yes' to delete all snapshots ({snapshots}):") != "yes":
            self.stdout.write("Canceled")
            return

        deleted, _ = PostSnapshot.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted snapshots: {deleted}"))
