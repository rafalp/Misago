import time

from django.core.management.base import BaseCommand, CommandError

from ....core.management.progressbar import show_progress
from ....parser.parse import parse
from ....threads.models import Post
from ...posts import posts_search


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

        posts = []
        posts_len = 0

        queryset = Post.objects.select_related("thread")
        for post in queryset.iterator(chunk_size=50):
            parsing_result = parse(post.content)

            posts.append((post, parsing_result.text))
            posts_len += 1

            if posts_len > 50:
                posts_search.index_posts(posts)
                posts = []
                posts_len = []

            rebuild_count += 1
            show_progress(self, rebuild_count, posts_to_reindex, start_time)

        if posts:
            posts_search.index_posts(posts)

        if rebuild_count == 1:
            self.stdout.write(f"\nRebuild search index for one post.")
        else:
            self.stdout.write(f"\nRebuild search index for {rebuild_count} posts.")
