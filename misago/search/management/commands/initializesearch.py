from django.core.management.base import BaseCommand

from ...exceptions import SearchBackendError
from ...posts import posts_search


class Command(BaseCommand):
    help = "Initializes search"

    def handle(self, *args, **options):
        try:
            posts_search.initialize()
        except SearchBackendError as exc:
            self.stderr.write(
                f'Error initializing search backend "{posts_search.backend.name}":'
                f"\n\n{exc}"
            )
        else:
            self.stdout.write(
                f"Initialized search backend: {posts_search.backend.name}"
            )
