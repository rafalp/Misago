import time

from django.core.management.base import BaseCommand

from misago.core.management.progressbar import show_progress
from misago.core.pgutils import batch_update
from misago.threads.models import Post


class Command(BaseCommand):
    help = "Rebuilds posts search"

    def handle(self, *args, **options):
        posts_to_sync = Post.objects.filter(is_event=False).count()

        if not posts_to_sync:
            self.stdout.write("\n\nNo posts were found")
        else:
            self.sync_threads(posts_to_sync)

    def sync_threads(self, posts_to_sync):
        message = "Rebuilding %s posts...\n"
        self.stdout.write(message % posts_to_sync)

        message = "\n\nRebuild %s posts"

        synchronized_count = 0
        show_progress(self, synchronized_count, posts_to_sync)
        start_time = time.time()

        queryset = Post.objects.select_related('thread').filter(is_event=False)
        for post in batch_update(queryset):
            if post.id == post.thread.first_post_id:
                post.set_search_document(post.thread.title)
            else:
                post.set_search_document()
            post.save(update_fields=['search_document'])

            post.update_search_vector()
            post.save(update_fields=['search_vector'])

            synchronized_count += 1
            show_progress(self, synchronized_count, posts_to_sync, start_time)

        self.stdout.write(message % synchronized_count)
