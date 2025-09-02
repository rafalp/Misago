import time

from django.core.management.base import BaseCommand

from ....core.management.progressbar import show_progress
from ....parser.parse import parse
from ....posts.models import Post


class Command(BaseCommand):
    help = "Rebuilds posts search"

    def handle(self, *args, **options):
        posts_to_reindex = Post.objects.filter(is_event=False).count()

        if not posts_to_reindex:
            self.stdout.write("\n\nNo posts were found")
        else:
            self.rebuild_posts_search(posts_to_reindex)

    def rebuild_posts_search(self, posts_to_reindex):
        self.stdout.write("Rebuilding search for %s posts...\n" % posts_to_reindex)

        rebuild_count = 0
        show_progress(self, rebuild_count, posts_to_reindex)
        start_time = time.time()

        queryset = Post.objects.select_related("thread").filter(is_event=False)
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

        self.stdout.write("\n\nRebuilt search for %s posts" % rebuild_count)
