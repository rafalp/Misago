from django.urls import path
from django.utils.translation import pgettext_lazy

from ..auth.decorators import login_required
from .views.edit import (
    PrivateThreadEditView,
    PrivateThreadPostEditView,
    ThreadEditView,
    ThreadPostEditView,
)
from .views.reply import (
    PrivateThreadReplyView,
    ThreadReplyView,
)
from .views.start import (
    PrivateThreadStartView,
    ThreadStartView,
)

urlpatterns = [
    path(
        "c/<slug:category_slug>/<int:category_id>/start/",
        login_required(
            pgettext_lazy(
                "thread start login required error",
                "Sign in to start new thread",
            )
        )(ThreadStartView.as_view()),
        name="thread-start",
    ),
    path(
        "private/start/",
        login_required(
            pgettext_lazy(
                "private thread start login required error",
                "Sign in to start new private thread",
            )
        )(PrivateThreadStartView.as_view()),
        name="private-thread-start",
    ),
    path(
        "t/<slug:thread_slug>/<int:thread_id>/reply/",
        login_required(
            pgettext_lazy(
                "thread reply login required error",
                "Sign in to reply to threads",
            )
        )(ThreadReplyView.as_view()),
        name="thread-reply",
    ),
    path(
        "p/<slug:thread_slug>/<int:thread_id>/reply/",
        login_required(
            pgettext_lazy(
                "thread reply login required error",
                "Sign in to reply to threads",
            )
        )(PrivateThreadReplyView.as_view()),
        name="private-thread-reply",
    ),
    path(
        "t/<slug:thread_slug>/<int:thread_id>/edit/",
        ThreadEditView.as_view(),
        name="thread-edit",
    ),
    path(
        "t/<slug:thread_slug>/<int:thread_id>/edit/<int:post_id>/",
        ThreadPostEditView.as_view(),
        name="thread-post-edit",
    ),
    path(
        "p/<slug:thread_slug>/<int:thread_id>/edit/",
        PrivateThreadEditView.as_view(),
        name="private-thread-edit",
    ),
    path(
        "p/<slug:thread_slug>/<int:thread_id>/edit/<int:post_id>/",
        PrivateThreadPostEditView.as_view(),
        name="private-thread-post-edit",
    ),
]
