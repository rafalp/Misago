import time

from django.core.management.base import BaseCommand, CommandError

from ....core.management.progressbar import show_progress
from ....parser.parse import parse
from ....threads.models import Post, Thread
from ...posts import PostsSearch, posts_search


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

        search_index = SearchIndexBuffer(posts_search, 50)

        queryset = Post.objects.select_related("thread")
        for post in queryset.iterator(chunk_size=50):
            if post.id == post.thread.first_post_id:
                search_index.index_thread(post.thread)

            search_index.index_post(post)

            rebuild_count += 1
            show_progress(self, rebuild_count, posts_to_reindex, start_time)

        search_index.commit_all()

        if rebuild_count == 1:
            self.stdout.write(f"\nRebuild search index for one post.")
        else:
            self.stdout.write(f"\nRebuild search index for {rebuild_count} posts.")


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
