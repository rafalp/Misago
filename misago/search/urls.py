from django.urls import path

from ..htmx.decorators import require_htmx
from ..plugins import extensions
from .decorators import private_threads_search_login_required
from .views import (
    PrivateThreadsQuickSearchView,
    PrivateThreadsSearchView,
    SearchView,
    ThreadsQuickSearchView,
    ThreadsSearchView,
    UsersQuickSearchView,
    UsersSearchView,
    UsersSuggestView,
)

search_view = extensions.get(SearchView).as_view()
threads_search_view = extensions.get(ThreadsSearchView).as_view()
threads_quick_search_view = extensions.get(ThreadsQuickSearchView).as_view()
private_threads_search_view = extensions.get(PrivateThreadsSearchView).as_view()
private_threads_quick_search_view = extensions.get(
    PrivateThreadsQuickSearchView
).as_view()
users_search_view = extensions.get(UsersSearchView).as_view()
users_quick_search_view = extensions.get(UsersQuickSearchView).as_view()
users_suggest_view = extensions.get(UsersSuggestView).as_view()

urlpatterns = [
    path("search/", search_view, name="search"),
    path("search/threads/", threads_search_view, name="threads-search"),
    path(
        "search/threads/quick/",
        require_htmx(threads_quick_search_view),
        name="threads-quick-search",
    ),
    path(
        "search/private-threads/",
        private_threads_search_login_required(private_threads_search_view),
        name="private-threads-search",
    ),
    path(
        "search/private-threads/quick/",
        require_htmx(
            private_threads_search_login_required(private_threads_quick_search_view)
        ),
        name="private-threads-quick-search",
    ),
    path("search/users/", users_search_view, name="users-search"),
    path(
        "search/users/quick/",
        require_htmx(users_quick_search_view),
        name="users-quick-search",
    ),
    path("search/users/suggest/", users_suggest_view, name="users-suggest"),
]
