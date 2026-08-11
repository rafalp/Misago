from enum import StrEnum


class SearchMode(StrEnum):
    THREADS = "threads"
    THREAD_TITLES = "thread_titles"
    POSTS = "posts"


class SearchOrder(StrEnum):
    RELEVANCE = "relevance"
    NEWEST = "newest"
