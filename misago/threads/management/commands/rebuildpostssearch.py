import time

from django.core.management.base import BaseCommand, CommandError

from ....core.management.progressbar import show_progress
from ....parser.parse import parse
from ...models import Post


class Command(BaseCommand):
    help = "Rebuilds posts search"

    def handle(self, *args, **options):
        posts_to_reindex = Post.objects.count()

        if not posts_to_reindex:
            raise CommandError("No posts exist.")

        if posts_to_reindex == 1:
            self.stdout.write("Rebuilding search for one post...\n")
        else:
            self.stdout.write(f"Rebuilding search for {posts_to_reindex} posts...\n")

        rebuild_count = 0
        show_progress(self, rebuild_count, posts_to_reindex)
        start_time = time.time()

        queryset = Post.objects.select_related("thread")
        for post in queryset.iterator(chunk_size=50):
            parsing_result = parse(post.original)

            if post.id == post.thread.first_post_id:
                post.search_document = f"{post.thread.title} {parsing_result.text}"
            else:
                post.search_document = parsing_result.text

            post.save(update_fields=["search_document"])

            post.set_search_vector()
            post.save(update_fields=["search_vector"])

            rebuild_count += 1
            show_progress(self, rebuild_count, posts_to_reindex, start_time)

        if rebuild_count == 1:
            self.stdout.write(f"\nRebuild search index for one post.")
        else:
            self.stdout.write(f"\nRebuild search index for {rebuild_count} posts.")
