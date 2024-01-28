import random
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....core.management.progressbar import show_progress
from ....notifications.models import Notification
from ....notifications.verbs import NotificationVerb
from ....threads.models import Post

User = get_user_model()


class Command(BaseCommand):
    help = "Adds notifications entries for all users and posts"

    def handle(self, *args, **options):
        total_users = User.objects.count()
        total_posts = Post.objects.count()

        self.stdout.write(
            f"Creating notifications entries for {total_users} users "
            f"and {total_posts} posts...\n"
        )

        Notification.objects.all().delete()

        total_notifications = total_users * total_posts
        processed_count = 0

        start_time = time.time()
        show_progress(self, processed_count, total_notifications)

        post_fields = (
            "id",
            "thread_id",
            "category_id",
            "thread__title",
            "poster_id",
            "poster_name",
            "posted_on",
        )

        for user in User.objects.iterator(chunk_size=50):
            for post in Post.objects.values(*post_fields).iterator(chunk_size=50):
                Notification.objects.create(
                    user=user,
                    category_id=post["category_id"],
                    thread_id=post["thread_id"],
                    thread_title=post["thread__title"],
                    post_id=post["id"],
                    actor_id=post["poster_id"],
                    actor_name=post["poster_name"],
                    verb=NotificationVerb.REPLIED,
                    is_read=random.choice((True, False)),
                    created_at=post["posted_on"],
                )

                processed_count += 1
                show_progress(self, processed_count, total_notifications)

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\nSuccessfully created %s notifications in %s"
        self.stdout.write(message % (total_notifications, total_humanized))
