from django.core.management.base import BaseCommand
from misago.forums.models import Forum

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few hours to reset deltas on forums
    """
    help = 'Clears users sessions'
    def handle(self, *args, **options):
        Forum.objects.all().update(threads_delta=0,posts_delta=0,redirects_delta=0)
        self.stdout.write('Forums deltas have been reset.\n')