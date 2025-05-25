from django.core.management.base import BaseCommand, CommandError
from misago.threads.models import Post

from ...models import PostSnapshot
from ...snapshots import restore_post_from_snapshot


class Command(BaseCommand):
    help = "Restores all posts from most recent snapshots"

    def handle(self, *args, **options):
        if input(f"Type 'yes' to restore all posts:") != "yes":
            self.stdout.write("Canceled")
            return

        restored = 0
        skipped = 0

        for post in Post.objects.order_by("-id").iterator():
            if self.handle_post(post):
                restored += 1
            else:
                skipped += 1

        self.stdout.write()
        self.stdout.write(f"Restored posts: {restored}")
        self.stdout.write(f"Skipped posts: {skipped}")

    def handle_post(self, post: Post):
        snapshot = PostSnapshot.objects.filter(post_id=post.id).order_by("id").last()
        if snapshot:
            restore_post_from_snapshot(post, snapshot)
            self.stdout.write(f"Restored post {post.id}")
            return True
        else:
            self.stdout.write(f"Post has no snapshot: {post.id}")
            return False
