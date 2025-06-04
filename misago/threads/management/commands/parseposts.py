import time

from django.core.management.base import BaseCommand

from ....core.management.progressbar import show_progress
from ....parser.parse import parse
from ...models import Post


class Command(BaseCommand):
    help = "Parses posts, updating their HTML, metadata and search"

    def handle(self, *args, **options):
        posts_to_parse = Post.objects.filter(is_event=False).count()

        if not posts_to_parse:
            self.stdout.write("\n\nNo posts were found")
        else:
            self.parse_posts(posts_to_parse)

    def parse_posts(self, posts_to_parse):
        self.stdout.write("Parsing %s posts...\n" % posts_to_parse)

        rebuild_count = 0
        show_progress(self, rebuild_count, posts_to_parse)
        start_time = time.time()

        queryset = Post.objects.select_related("thread").filter(is_event=False)
        for post in queryset.iterator(chunk_size=50):
            parsing_result = parse(post.original)

            post.parsed = parsing_result.html
            post.metadata = parsing_result.metadata
            post.set_search_document(post.thread, parsing_result.text)
            post.save(update_fields=["parsed", "metadata", "search_document"])

            post.set_search_vector()
            post.save(update_fields=["search_vector"])

            rebuild_count += 1
            show_progress(self, rebuild_count, posts_to_parse, start_time)

        self.stdout.write("\n\nParsed %s posts" % rebuild_count)
