from time import time

from django.core.management.base import BaseCommand

from ...exceptions import SearchBackendError
from ...service import search


class Command(BaseCommand):
    help = "Clears search data."

    def handle(self, *args, **options):
        try:
            start_time = time()
            search.clear()
        except SearchBackendError as exc:
            self.stderr.write(
                f'Error clearing search using "{search.backend.name}":\n\n{exc}'
            )
        else:
            total_time = "{:.2f}s".format(time() - start_time)
            self.stdout.write(
                f'Cleared data from "{search.backend.name}" in {total_time}.'
            )
