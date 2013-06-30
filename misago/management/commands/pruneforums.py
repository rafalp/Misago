from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from misago.models import Forum, Thread, Post
from misago.monitor import monitor, UpdatingMonitor

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few days to run forums pruning policies
    """
    help = 'Updates Popular Threads ranking'
    def handle(self, *args, **options):
        sync_forums = []
        for forum in Forum.objects.all():
            archive = forum.pruned_archive
            deleted = 0
            if forum.prune_start:
                for thread in forum.thread_set.filter(weight=0).filter(start__lte=timezone.now() - timedelta(days=forum.prune_start)):
                    if archive:
                        thread.move_to(archive)
                        thread.save(force_update=True)
                    else:
                        thread.delete()                        
                    deleted += 1
            if forum.prune_last:
                for thread in forum.thread_set.filter(weight=0).filter(last__lte=timezone.now() - timedelta(days=forum.prune_last)):
                    if archive:
                        thread.move_to(archive)
                        thread.save(force_update=True)
                    else:
                        thread.delete()
                    deleted += 1
            if deleted:
                if forum not in sync_forums:
                    sync_forums.append(forum)
                if archive and archive not in sync_forums:
                    sync_forums.append(archive)
        for forum in sync_forums:
            forum.sync()
            forum.save(force_update=True)

        with UpdatingMonitor() as cm:
            monitor.threads = Thread.objects.count()
            monitor.posts = Post.objects.count()
        self.stdout.write('Forums were pruned.\n')