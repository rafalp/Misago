from ...pagetype import create_page_type
from .post import post_type
from .query import query_type
from .searchresults import search_results_type
from .thread import thread_type
from .threadedge import thread_edge_type
from .threadspage import threads_page_type

types = [
    create_page_type("PostsPage"),
    post_type,
    query_type,
    search_results_type,
    thread_type,
    thread_edge_type,
    threads_page_type,
]
