from .generic import PrivateThreadView

from django.http import HttpRequest
from django.db.models import QuerySet

from ...categories.enums import CategoryTree
from ...posts.models import Post
from ...posts.redirect import redirect_to_post
from ...posts.views.redirect import (
    LastPostRedirectView,
    PostRedirectView,
    UnapprovedPostRedirectView,
    UnreadPostRedirectView,
)
from ...threads.models import Thread
from .generic import PrivateThreadView


class PrivateThreadLastPostRedirectView(LastPostRedirectView, PrivateThreadView):
    pass


class PrivateThreadUnreadPostRedirectView(UnreadPostRedirectView, PrivateThreadView):
    pass


class PrivateThreadUnapprovedPostRedirectView(
    UnapprovedPostRedirectView, PrivateThreadView
):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_private_threads_moderator:
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class PrivateThreadPostRedirectView(PostRedirectView, PrivateThreadView):
    pass


redirect_to_post.view(
    CategoryTree.PRIVATE_THREADS, PrivateThreadPostRedirectView.as_view()
)
