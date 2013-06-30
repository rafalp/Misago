from django.core.management.base import BaseCommand
from misago.models import Post
from misago.monitor import monitor

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few minutes/hours to count reported posts
    """
    help = 'Counts reported posts'
    def handle(self, *args, **options):
        monitor['reported_posts'] = Post.objects.filter(reported=True).count()
        self.stdout.write('Reported posts were recounted.\n')