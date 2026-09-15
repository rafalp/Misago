from django.urls import path

from ..plugins import extensions
from .views import (
    PrivateThreadsSearchView,
    SearchView,
    ThreadsSearchView,
    UsersSearchView,
)

search_view = extensions.get(SearchView).as_view()
threads_search_view = extensions.get(ThreadsSearchView).as_view()
private_threads_search_view = extensions.get(PrivateThreadsSearchView).as_view()
users_search_view = extensions.get(UsersSearchView).as_view()

urlpatterns = [
    path("search/", search_view, name="search"),
    path("search/threads/", threads_search_view, name="threads-search"),
    path(
        "search/private-threads/",
        private_threads_search_view,
        name="private-threads-search",
    ),
    path("search/users/", users_search_view, name="users-search"),
]
