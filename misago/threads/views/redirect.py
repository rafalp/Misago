from django.http import HttpRequest
from django.db.models import QuerySet

from ...categories.enums import CategoryTree
from ...posts.models import Post
from ...posts.redirect import redirect_to_post
from ...posts.views.redirect import (
    LastPostRedirectView,
    PostRedirectView,
    SolutionRedirectView,
    UnapprovedPostRedirectView,
    UnreadPostRedirectView,
)
from ..models import Thread
from .generic import ThreadView


class ThreadLastPostRedirectView(LastPostRedirectView, ThreadView):
    pass


class ThreadUnreadPostRedirectView(UnreadPostRedirectView, ThreadView):
    pass


class ThreadSolutionRedirectView(SolutionRedirectView, ThreadView):
    pass


class ThreadUnapprovedPostRedirectView(UnapprovedPostRedirectView, ThreadView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_category_moderator(thread.category_id):
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class ThreadPostRedirectView(PostRedirectView, ThreadView):
    pass


redirect_to_post.view(CategoryTree.THREADS, ThreadPostRedirectView.as_view())
