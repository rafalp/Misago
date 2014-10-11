from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.forums.models import Forum


class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired
    every few days to run forums pruning policies
    """
    help = 'Prunes forums'

    def handle(self, *args, **options):
        now = timezone.now()
        synchronize_forums = []

        for forum in Forum.objects.iterator():
            archive = forum.archive_pruned_in
            pruned_threads = 0

            threads_qs = forum.thread_set.filter(is_pinned=False)

            if forum.prune_started_after:
                cutoff = now - timedelta(days=forum.prune_started_after)
                prune_qs = threads_qs.filter(started_on__lte=cutoff)
                for thread in prune_qs.iterator():
                    if archive:
                        thread.move(archive)
                        thread.save()
                    else:
                        thread.delete()
                    pruned_threads += 1

            if forum.prune_replied_after:
                cutoff = now - timedelta(days=forum.prune_replied_after)
                prune_qs = threads_qs.filter(last_post_on__lte=cutoff)
                for thread in prune_qs.iterator():
                    if archive:
                        thread.move(archive)
                        thread.save()
                    else:
                        thread.delete()
                    pruned_threads += 1

            if pruned_threads:
                if forum not in synchronize_forums:
                    synchronize_forums.append(forum)
                if archive and archive not in synchronize_forums:
                    synchronize_forums.append(archive)

        for forum in synchronize_forums:
            forum.synchronize()
            forum.save()

        self.stdout.write('Forums were pruned.\n')
