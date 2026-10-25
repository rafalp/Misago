from time import time

from django.core.management.base import BaseCommand

from ...exceptions import ThreadsSearchBackendError
from ...threads import threads_search


class Command(BaseCommand):
    help = "Clears search data."

    def handle(self, *args, **options):
        try:
            start_time = time()
            threads_search.clear()
        except ThreadsSearchBackendError as exc:
            self.stderr.write(
                f'Error clearing search using "{threads_search.backend.name}":\n\n{exc}'
            )
        else:
            total_time = "{:.2f}s".format(time() - start_time)
            self.stdout.write(
                f'Cleared data from "{threads_search.backend.name}" in {total_time}.'
            )
