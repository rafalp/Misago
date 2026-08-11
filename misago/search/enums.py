from enum import StrEnum


class SearchMode(StrEnum):
    THREADS = "threads"
    POSTS = "posts"


class SearchOrder(StrEnum):
    RELEVANCE = "relevance"
    NEWEST = "newest"
