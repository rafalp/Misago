from django.core.management.base import BaseCommand, CommandError
from misago.threads.models import Post

from ...snapshots import create_post_snapshot


class Command(BaseCommand):
    help = "Creates post snapshots"

    def add_arguments(self, parser):
        parser.add_argument("post_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for post_id in options["post_ids"]:
            self.handle_post_id(post_id)

    def handle_post_id(self, post_id: str):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise CommandError(f"Post {post_id} does not exist")

        create_post_snapshot(post)

        self.stdout.write(
            self.style.SUCCESS(f"Created new snapshot for post {post.id}")
        )
