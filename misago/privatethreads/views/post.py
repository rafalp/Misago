from django.db.models import QuerySet
from django.http import HttpRequest

from ...categories.enums import CategoryTree
from ...threads.models import Post, Thread
from ...threads.redirect import redirect_to_post
from ...threads.views import (
    PostLastView,
    PostUnapprovedView,
    PostUnreadView,
    PostView,
)
from ..threadtypes import private_thread_type


class PrivateThreadPostLastView(PostLastView):
    thread_type = private_thread_type


class PrivateThreadPostUnapprovedView(PostUnapprovedView):
    thread_type = private_thread_type

    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_private_threads_moderator:
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class PrivateThreadPostUnreadView(PostUnreadView):
    thread_type = private_thread_type


class PrivateThreadPostView(PostView):
    thread_type = private_thread_type


redirect_to_post.view(CategoryTree.PRIVATE_THREADS, PrivateThreadPostView.as_view())
