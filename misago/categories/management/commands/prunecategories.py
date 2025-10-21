from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ....threads.move import move_threads
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
        pruned_categories = []

        for category in Category.objects.order_by("lft").iterator():
            if not (category.prune_started_after or category.prune_replied_after):
                continue

            pruned_categories.append(category)

            archive = category.archive_pruned_in
            pruned_threads = 0

            threads_qs = category.thread_set.filter(weight=0)

            if category.prune_started_after:
                cutoff = now - timedelta(days=category.prune_started_after)
                prune_qs = threads_qs.filter(started_at__lte=cutoff)
                for thread in prune_qs.iterator(chunk_size=50):
                    if archive:
                        move_threads(thread, archive)
                    else:
                        thread.delete()
                    pruned_threads += 1

            if category.prune_replied_after:
                cutoff = now - timedelta(days=category.prune_replied_after)
                prune_qs = threads_qs.filter(last_posted_at__lte=cutoff)
                for thread in prune_qs.iterator(chunk_size=50):
                    if archive:
                        move_threads(thread, archive)
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

        self.stdout.write(f"\n\nPruned categories: {len(pruned_categories)}")
        if pruned_categories:
            self.stdout.write("")

        for category in pruned_categories:
            self.stdout.write(f"- #{category.id}: {category.name}")
