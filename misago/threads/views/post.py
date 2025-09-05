from django.http import HttpRequest
from django.db.models import QuerySet

from ...categories.enums import CategoryTree
from ...posts.models import Post
from ...posts.redirect import redirect_to_post
from ...posts.views.post import (
    PostLastView,
    PostSolutionView,
    PostUnapprovedView,
    PostUnreadView,
    PostView,
)
from ..models import Thread
from .generic import ThreadView


class ThreadPostLastView(PostLastView, ThreadView):
    pass


class ThreadPostSolutionView(PostSolutionView, ThreadView):
    pass


class ThreadPostUnreadView(PostUnreadView, ThreadView):
    pass


class ThreadPostUnapprovedView(PostUnapprovedView, ThreadView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_category_moderator(thread.category_id):
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class ThreadPostView(PostView, ThreadView):
    pass


redirect_to_post.view(CategoryTree.THREADS, ThreadPostView.as_view())
