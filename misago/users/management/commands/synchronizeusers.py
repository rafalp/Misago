import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.categories.models import Category
from misago.core.management.progressbar import show_progress
from misago.core.pgutils import batch_update


UserModel = get_user_model()


class Command(BaseCommand):
    help = "Synchronizes users"

    def handle(self, *args, **options):
        users_to_sync = UserModel.objects.count()

        if not users_to_sync:
            self.stdout.write("\n\nNo users were found")
        else:
            self.sync_users(users_to_sync)

    def sync_users(self, users_to_sync):
        categories = Category.objects.root_category().get_descendants()

        message = "Synchronizing %s users...\n"
        self.stdout.write(message % users_to_sync)

        synchronized_count = 0
        show_progress(self, synchronized_count, users_to_sync)
        start_time = time.time()
        for user in batch_update(UserModel.objects.all()):
            user.threads = user.thread_set.filter(
                category__in=categories,
                is_hidden=False,
                is_unapproved=False,
            ).count()

            user.posts = user.post_set.filter(
                category__in=categories,
                is_event=False,
                is_unapproved=False,
            ).count()

            user.followers = user.followed_by.count()
            user.following = user.follows.count()

            user.save()

            synchronized_count += 1
            show_progress(self, synchronized_count, users_to_sync, start_time)

        self.stdout.write("\n\nSynchronized %s users" % synchronized_count)
