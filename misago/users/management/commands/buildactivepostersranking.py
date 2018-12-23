from time import time

from django.core.management.base import BaseCommand

from ...activepostersranking import build_active_posters_ranking


class Command(BaseCommand):
    help = "Builds active posters ranking"

    def handle(self, *args, **options):
        self.stdout.write("\nBuilding active posters ranking...")

        start_time = time()
        build_active_posters_ranking()
        end_time = time() - start_time

        self.stdout.write("Finished after %.2fs" % end_time)
