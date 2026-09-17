from time import time

from django.core.management.base import BaseCommand

from ...exceptions import SearchBackendError
from ...search import search


class Command(BaseCommand):
    help = "Clears search"

    def handle(self, *args, **options):
        try:
            start_time = time()
            search.clear()
        except SearchBackendError as exc:
            self.stderr.write(
                f'Error clearing the search index using the "{search.backend.name}" backend:'
                f"\n\n{exc}"
            )
        else:
            total_time = "{:.2f}s".format(time() - start_time)
            self.stdout.write(
                f'Cleared the search index using the "{search.backend.name}" backend.'
                f"\n\nTime: {total_time}"
            )
