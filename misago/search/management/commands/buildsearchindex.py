from time import time

from django.core.management.base import BaseCommand, CommandError

from ....core.management.progressbar import show_progress
from ....parser.parse import parse
from ....threads.models import Post, Thread
from ...exceptions import SearchBackendError
from ...posts import PostsSearch, posts_search


class Command(BaseCommand):
    help = "Builds search index"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-clear",
            action="store_true",
            help="Skip clearing of existing search data.",
        )

    def handle(self, *args, **options):
        post_count = Post.objects.count()

        self.stdout.write(
            'Rebuilding the search index using the '
            f'"{posts_search.backend.name}" backend.'
            "\n\n"
        )

        if options["skip_clear"]:
            self.stdout.write(f"Skipped clearing the search index.\n\n"
            )
        else:
            try:
                start_time = time()
                posts_search.clear()
            except SearchBackendError as exc:
                self.stderr.write(f"\nError clearing the search index:\n\n{exc}")
                return
            else:
                total_time = "{:.2f}s".format(time() - start_time)
                self.stdout.write(f"Cleared the search index in {total_time}.\n\n")

        if not post_count:
            raise CommandError("No posts exist.")

        if post_count == 1:
            self.stdout.write("Indexing one post...\n")
        else:
            self.stdout.write(f"Indexing {post_count} posts...\n")

        indexed_count = 0
        show_progress(self, indexed_count, post_count)
        start_time = time()

        search_index = SearchIndexBuffer(posts_search, 50)

        queryset = Post.objects.select_related("thread").order_by("id")
        for post in queryset.iterator(chunk_size=50):
            if post.id == post.thread.first_post_id:
                search_index.index_thread(post.thread)

            search_index.index_post(post)

            indexed_count += 1
            show_progress(self, indexed_count, post_count, start_time)

        search_index.commit_all()
        total_time = "{:.2f}s".format(time() - start_time)

        if indexed_count == 1:
            self.stdout.write(f"\n\nIndexed one post in {total_time}.")
        else:
            self.stdout.write(f"\n\nIndexed {indexed_count} posts in {total_time}.")


class SearchIndexBuffer:
    search: PostsSearch
    max_size: int

    threads: list[Thread]
    threads_size: int

    posts: list[Post]
    posts_size: int

    def __init__(self, search: PostsSearch, max_size: int):
        self.search = search
        self.max_size = max_size

        self.threads = []
        self.threads_size = 0

        self.posts = []
        self.posts_size = 0

    def index_thread(self, thread: Thread):
        self.threads.append(thread)
        self.threads_size += 1

        if self.threads_size >= self.max_size:
            self.commit_threads()

    def index_post(self, post: Post):
        self.posts.append(post)
        self.posts_size += 1

        if self.posts_size >= self.max_size:
            self.commit_posts()

    def commit_threads(self):
        if self.threads:
            self.search.index_threads(self.threads)
            self.threads = []
            self.threads_size = 0

    def commit_posts(self):
        if self.posts:
            self.search.index_posts(
                (post, parse(post.content).text) for post in self.posts
            )
            self.posts = []
            self.posts_size = 0

    def commit_all(self):
        self.commit_threads()
        self.commit_posts()
