from django.core.management.base import BaseCommand
from django.db.models import F
from misago.conf import settings
from misago.models import Thread

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few days to update thread popularity ranking
    """
    help = 'Updates Popular Threads ranking'
    def handle(self, *args, **options):
        if settings.thread_ranking_inflation > 0:
            inflation = float(100 - settings.thread_ranking_inflation) / 100
            Thread.objects.all().update(score=F('score') * inflation)
            self.stdout.write('Thread ranking has been updated.\n')
        else:
            self.stdout.write('Thread ranking inflation is disabled.\n')
