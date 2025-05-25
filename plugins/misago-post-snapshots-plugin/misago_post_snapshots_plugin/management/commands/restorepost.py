from django.core.management.base import BaseCommand, CommandError
from misago.threads.models import Post

from ...models import PostSnapshot
from ...snapshots import restore_post_from_snapshot


class Command(BaseCommand):
    help = "Restores post from snapshot"

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

        snapshots = list(PostSnapshot.objects.filter(post_id=post.id).order_by("-id"))
        if not snapshots:
            raise CommandError(f"Post {post_id} has no snapshots")
        elif len(snapshots) == 1:
            restore_post_from_snapshot(post, snapshots[0])
            self.stdout.write(
                self.style.SUCCESS(f"Restored post {post.id} from snapshot #1")
            )
        else:
            self.stdout.write(f"Select snapshot to restore the post {post.id}:")
            self.stdout.write()

            for i, snapshot in enumerate(snapshots):
                self.stdout.write(f"{i + 1} - {snapshot.created_at}")

            self.stdout.write()

            try:
                choice = int(input("Choice:"))
                if choice < 1 or choice > len(snapshots):
                    raise CommandError("Wrong choice")
            except (TypeError, ValueError):
                pass

            restore_post_from_snapshot(post, snapshots[choice - 1])
            self.stdout.write(
                self.style.SUCCESS(f"Restored post {post.id} from snapshot #{choice}")
            )
