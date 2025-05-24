from django.core.management.base import BaseCommand, CommandError
from misago.threads.models import Post

from ...snapshot import create_post_snapshot


class Command(BaseCommand):
    help = "Creates snapshots for all posts"

    def handle(self, *args, **options):
        for post in Post.objects.order_by("-id").iterator():
            create_post_snapshot(post)
            self.stdout.write(
                self.style.SUCCESS(f"Created new snapshot for post {post.id}")
            )
