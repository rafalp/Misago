from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Category


class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired
    every few days (or more often) to execute categories pruning policies
    """

    help = "Prunes categories"

    def handle(self, *args, **options):  # pylint: disable=too-many-branches
        now = timezone.now()
        synchronize_categories = []

        for category in Category.objects.iterator():
            archive = category.archive_pruned_in
            pruned_threads = 0

            threads_qs = category.thread_set.filter(weight=0)

            if category.prune_started_after:
                cutoff = now - timedelta(days=category.prune_started_after)
                prune_qs = threads_qs.filter(started_on__lte=cutoff)
                for thread in prune_qs.iterator():
                    if archive:
                        thread.move(archive)
                        thread.save()
                    else:
                        thread.delete()
                    pruned_threads += 1

            if category.prune_replied_after:
                cutoff = now - timedelta(days=category.prune_replied_after)
                prune_qs = threads_qs.filter(last_post_on__lte=cutoff)
                for thread in prune_qs.iterator():
                    if archive:
                        thread.move(archive)
                        thread.save()
                    else:
                        thread.delete()
                    pruned_threads += 1

            if pruned_threads:
                if category not in synchronize_categories:
                    synchronize_categories.append(category)
                if archive and archive not in synchronize_categories:
                    synchronize_categories.append(archive)

        for category in synchronize_categories:
            category.synchronize()
            category.save()

        self.stdout.write("\n\nCategories were pruned")
