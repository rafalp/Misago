from enum import StrEnum

from django.utils.translation import pgettext_lazy


class SearchMode(StrEnum):
    THREAD_TITLES = "thread_titles"
    THREADS = "threads"
    POSTS = "posts"

    @classmethod
    def get_choices(cls):
        return (
            (cls.THREADS, pgettext_lazy("search mode", "Threads")),
            (cls.POSTS, pgettext_lazy("search mode", "Posts")),
            (cls.THREAD_TITLES, pgettext_lazy("search mode", "Thread titles")),
        )


class SearchSort(StrEnum):
    RELEVANCE = "relevance"
    NEWEST = "newest"

    @classmethod
    def get_choices(cls):
        return (
            (cls.RELEVANCE, pgettext_lazy("search sort", "Relevance")),
            (cls.NEWEST, pgettext_lazy("search sort", "Newest")),
        )
