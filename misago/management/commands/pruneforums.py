from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from misago.models import Forum, Thread, Post
from misago.monitor import Monitor

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few days to run forums pruning policies
    """
    help = 'Updates Popular Threads ranking'
    def handle(self, *args, **options):
        for forum in Forum.objects.all():
            deleted = 0
            if forum.prune_start:
                for thread in forum.thread_set.filter(weight=0).filter(start__lte=timezone.now() - timedelta(days=forum.prune_start)):
                    thread.delete()
                    deleted += 1
            if forum.prune_last:
                for thread in forum.thread_set.filter(weight=0).filter(last__lte=timezone.now() - timedelta(days=forum.prune_last)):
                    thread.delete()
                    deleted += 1
            if deleted:
                forum.sync()
                forum.save(force_update=True)
        monitor = Monitor()
        monitor['threads'] = Post.objects.count()
        monitor['posts'] = Post.objects.count()
        self.stdout.write('Forums were pruned.\n')