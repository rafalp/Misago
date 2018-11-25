from django.core.management.base import BaseCommand

from misago.cache.versions import invalidate_all


class Command(BaseCommand):
    help = 'Invalidates versioned caches'

    def handle(self, *args, **options):
        invalidate_all()
        self.stdout.write("Invalidated versioned caches.")
