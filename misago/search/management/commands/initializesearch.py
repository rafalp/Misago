from time import time

from django.core.management.base import BaseCommand

from ...exceptions import SearchBackendError
from ...service import search


class Command(BaseCommand):
    help = "Initializes search."

    def handle(self, *args, **options):
        try:
            start_time = time()
            search.initialize()
        except SearchBackendError as exc:
            self.stderr.write(f'Error initializing "{search.backend.name}":\n\n{exc}')
        else:
            total_time = "{:.2f}s".format(time() - start_time)
            self.stdout.write(f'Initialized "{search.backend.name}" in {total_time}.')
