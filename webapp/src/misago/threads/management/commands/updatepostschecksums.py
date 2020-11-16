import time

from django.core.management.base import BaseCommand

from ....core.management.progressbar import show_progress
from ....core.pgutils import chunk_queryset
from ...checksums import update_post_checksum
from ...models import Post


class Command(BaseCommand):
    help = "Updates posts checksums"

    def handle(self, *args, **options):
        posts_to_update = Post.objects.filter(is_event=False).count()

        if not posts_to_update:
            self.stdout.write("\n\nNo posts were found")
        else:
            self.update_posts_checksums(posts_to_update)

    def update_posts_checksums(self, posts_to_update):
        self.stdout.write("Updating %s posts checksums...\n" % posts_to_update)

        updated_count = 0
        show_progress(self, updated_count, posts_to_update)
        start_time = time.time()

        queryset = Post.objects.filter(is_event=False)
        for post in chunk_queryset(queryset):
            update_post_checksum(post)
            post.save(update_fields=["checksum"])

            updated_count += 1
            show_progress(self, updated_count, posts_to_update, start_time)

        self.stdout.write("\n\nUpdated %s posts checksums" % updated_count)
