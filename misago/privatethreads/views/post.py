from .generic import PrivateThreadView

from django.http import HttpRequest
from django.db.models import QuerySet

from ...categories.enums import CategoryTree
from ...posts.models import Post
from ...posts.redirect import redirect_to_post
from ...posts.views.post import (
    PostLastView,
    PostUnapprovedView,
    PostUnreadView,
    PostView,
)
from ...threads.models import Thread
from .generic import PrivateThreadView


class PrivateThreadPostLastView(PostLastView, PrivateThreadView):
    pass


class PrivateThreadPostUnreadView(PostUnreadView, PrivateThreadView):
    pass


class PrivateThreadPostUnapprovedView(PostUnapprovedView, PrivateThreadView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_private_threads_moderator:
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class PrivateThreadPostView(PostView, PrivateThreadView):
    pass


redirect_to_post.view(CategoryTree.PRIVATE_THREADS, PrivateThreadPostView.as_view())
