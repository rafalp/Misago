from enum import StrEnum


class SearchMode(StrEnum):
    THREAD_TITLES = "thread_titles"
    THREADS = "threads"
    POSTS = "posts"


class SearchOrder(StrEnum):
    RELEVANCE = "relevance"
    NEWEST = "newest"
