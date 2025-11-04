import time

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from ....core.management.progressbar import show_progress
from ....threads.models import Post
from ...models import Like
from ...synchronize import synchronize_post_likes


class Command(BaseCommand):
    help = "Synchronizes post likes"

    def handle(self, *args, **options):
        self.sync_post_with_likes()
        self.sync_posts_without_likes()

    def sync_post_with_likes(self):
        posts_queryset = Post.objects.filter(id__in=Like.objects.values("post_id"))

        posts_to_sync = posts_queryset.count()
        if posts_to_sync == 1:
            self.stdout.write("Synchronizing one post...\n")
        else:
            self.stdout.write(f"Synchronizing {posts_to_sync} posts...\n")

        if not posts_to_sync:
            self.stdout.write(f"\nSynchronized {posts_to_sync} posts with likes.")
            return

        synchronized_count = 0
        show_progress(self, synchronized_count, posts_to_sync)
        start_time = time.time()

        for post in Post.objects.iterator(chunk_size=50):
            synchronize_post_likes(post)

            synchronized_count += 1
            show_progress(self, synchronized_count, posts_to_sync, start_time)

        if posts_to_sync == 1:
            self.stdout.write(f"\nSynchronized one post with likes.")
        else:
            self.stdout.write(f"\nSynchronized {posts_to_sync} posts with likes.")

    def sync_posts_without_likes(self):
        cleared_posts = (
            Post.objects.filter(Q(likes__gt=0) | Q(last_likes__isnull=False))
            .exclude(id__in=Like.objects.values("post_id"))
            .update(likes=0, last_likes=None)
        )

        if cleared_posts == 1:
            self.stdout.write(f"\nRemoved outdated likes data from one post.")
        else:
            self.stdout.write(
                f"\nRemoved outdated likes data from {cleared_posts} posts."
            )
