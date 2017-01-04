import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.core.management.progressbar import show_progress
from misago.core.pgutils import batch_update


class Command(BaseCommand):
    help = 'Synchronizes users'

    def handle(self, *args, **options):
        users_to_sync = get_user_model().objects.count()

        if not users_to_sync:
            self.stdout.write('\n\nNo users were found')
        else:
            self.sync_users(users_to_sync)

    def sync_users(self, users_to_sync):
        message = 'Synchronizing %s users...\n'
        self.stdout.write(message % users_to_sync)

        message = '\n\nSynchronized %s users'

        synchronized_count = 0
        show_progress(self, synchronized_count, users_to_sync)
        start_time = time.time()
        for user in batch_update(get_user_model().objects.all()):
            user.threads = user.thread_set.filter(is_unapproved=False).count()
            user.posts = user.post_set.filter(is_unapproved=False).count()
            user.followers = user.followed_by.count()
            user.following = user.follows.count()
            user.save()

            synchronized_count += 1
            show_progress(self, synchronized_count, users_to_sync, start_time)

        self.stdout.write(message % synchronized_count)
