from django.core.management.base import BaseCommand

from ...exceptions import SearchBackendError
from ...search import search


class Command(BaseCommand):
    help = "Initializes search"

    def handle(self, *args, **options):
        try:
            search.initialize()
        except SearchBackendError as exc:
            self.stderr.write(
                f'Error initializing the search backend "{search.backend.name}":'
                f"\n\n{exc}"
            )
        else:
            self.stdout.write(f"Initialized the search backend: {search.backend.name}")
