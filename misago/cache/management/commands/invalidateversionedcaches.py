from django.core.management.base import BaseCommand

from misago.cache.cache import invalidate_all_caches


class Command(BaseCommand):
    help = 'Invalidates versioned caches'

    def handle(self, *args, **options):
        invalidate_all_caches()
        self.stdout.write("Invalidated all versioned caches.")
