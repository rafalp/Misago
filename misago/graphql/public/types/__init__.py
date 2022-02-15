from ...pagetype import create_page_type
from .category import category_type
from .post import post_type
from .postdeleteresult import (
    post_delete_mutation_result,
    posts_bulk_delete_mutation_result,
)
from .query import query_type
from .searchresults import search_results_type
from .thread import thread_type
from .threadedge import thread_edge_type
from .threadspage import threads_page_type

types = [
    create_page_type("PostsPage"),
    category_type,
    post_type,
    post_delete_mutation_result,
    posts_bulk_delete_mutation_result,
    query_type,
    search_results_type,
    thread_type,
    thread_edge_type,
    threads_page_type,
]
