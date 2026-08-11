from time import time

from django.core.management.base import BaseCommand

from ...exceptions import SearchBackendError
from ...posts import posts_search


class Command(BaseCommand):
    help = "Clears search"

    def handle(self, *args, **options):
        try:
            start_time = time()
            posts_search.clear()
        except SearchBackendError as exc:
            self.stderr.write(
                f'Error clearing search index using the "{posts_search.backend.name}" backend:'
                f"\n\n{exc}"
            )
        else:
            total_time = "{:.2f}s".format(time() - start_time)
            self.stdout.write(
                f'Cleared search index using the "{posts_search.backend.name}" backend.'
                f"\n\nTime: {total_time}"
            )
