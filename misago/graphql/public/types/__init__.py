from .pagination import pagination_type
from .post import post_type
from .query import query_type
from .searchresults import search_results_type
from .thread import thread_type
from .threadposts import thread_posts_type
from .threadsfeed import threads_feed_type

types = [
    pagination_type,
    post_type,
    query_type,
    search_results_type,
    thread_posts_type,
    thread_type,
    threads_feed_type,
]
