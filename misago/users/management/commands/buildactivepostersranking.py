from django.core.management.base import BaseCommand

from misago.users.activepostersranking import build_active_posters_ranking


class Command(BaseCommand):
    help = 'Builds active posters ranking'

    def handle(self, *args, **options):
        self.stdout.write('\n\nBuilding active posters ranking...')
        build_active_posters_ranking()
        self.stdout.write('Done!')
