import time

from django.core.management.base import BaseCommand, CommandError

from ....core.management.progressbar import show_progress
from ....parser.parse import parse
from ...models import Post


class Command(BaseCommand):
    help = "Parses posts, updating their HTML, metadata and search"

    def handle(self, *args, **options):
        posts_to_parse = Post.objects.count()

        if not posts_to_parse:
            raise CommandError("No posts exist.")

        if posts_to_parse == 1:
            self.stdout.write("Parsing one post...\n")
        else:
            self.stdout.write(f"Parsing {posts_to_parse} posts...\n")

        rebuild_count = 0
        show_progress(self, rebuild_count, posts_to_parse)
        start_time = time.time()

        queryset = Post.objects.select_related("thread")
        for post in queryset.iterator(chunk_size=50):
            parsing_result = parse(post.content)

            post.content = parsing_result.markup
            post.content_parsed = parsing_result.html
            post.metadata = parsing_result.metadata
            post.save(
                update_fields=[
                    "content",
                    "content_parsed",
                    "metadata",
                ]
            )

            rebuild_count += 1
            show_progress(self, rebuild_count, posts_to_parse, start_time)

        if rebuild_count == 1:
            self.stdout.write(f"\nParsed one post.")
        else:
            self.stdout.write(f"\nParsed {rebuild_count} posts.")
