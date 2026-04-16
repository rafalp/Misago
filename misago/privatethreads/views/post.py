from django.db.models import QuerySet
from django.http import HttpRequest

from .generic import PrivateThreadView

from ...categories.enums import CategoryTree
from ...threads.models import Post, Thread
from ...threads.redirect import redirect_to_post
from ...threads.views.post import (
    PostLastView,
    PostUnapprovedView,
    PostUnreadView,
    PostView,
)
from .generic import PrivateThreadView


class PrivateThreadPostLastView(PostLastView, PrivateThreadView):
    pass


class PrivateThreadPostUnapprovedView(PostUnapprovedView, PrivateThreadView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_private_threads_moderator:
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class PrivateThreadPostUnreadView(PostUnreadView, PrivateThreadView):
    pass


class PrivateThreadPostView(PostView, PrivateThreadView):
    pass


redirect_to_post.view(CategoryTree.PRIVATE_THREADS, PrivateThreadPostView.as_view())
