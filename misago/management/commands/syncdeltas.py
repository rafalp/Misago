from django.core.management.base import BaseCommand
from django.db.models import F
from misago.models import Forum

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few hours to update threads/posts/clicks history on forum
    """
    help = 'Clears users sessions'
    def handle(self, *args, **options):
        Forum.objects.all().update(threads_delta=F('threads'), posts_delta=F('posts'), redirects_delta=F('redirects'))
        self.stdout.write('Forums deltas have been synced.\n')
