from django.urls import path
from django.utils.translation import pgettext_lazy

from ..auth.decorators import login_required
from ..plugins import extensions
from .views.categoryselect import ThreadStartCategorySelectView
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

thread_start_category_select_view = extensions.get(
    ThreadStartCategorySelectView
).as_view()
thread_start_view = extensions.get(ThreadStartView).as_view()
thread_reply_view = extensions.get(ThreadReplyView).as_view()
thread_edit_view = extensions.get(ThreadEditView).as_view()
thread_post_edit_view = extensions.get(ThreadPostEditView).as_view()

private_thread_start_view = extensions.get(PrivateThreadStartView).as_view()
private_thread_reply_view = extensions.get(PrivateThreadReplyView).as_view()
private_thread_edit_view = extensions.get(PrivateThreadEditView).as_view()
private_thread_post_edit_view = extensions.get(PrivateThreadPostEditView).as_view()

urlpatterns = [
    path(
        "threads/start/",
        thread_start_category_select_view,
        name="thread-start",
    ),
    path(
        "c/<slug:slug>/<int:category_id>/start/",
        login_required(
            pgettext_lazy(
                "thread start login required error",
                "Sign in to start new thread",
            )
        )(thread_start_view),
        name="thread-start",
    ),
    path(
        "private/start/",
        login_required(
            pgettext_lazy(
                "private thread start login required error",
                "Sign in to start new private thread",
            )
        )(private_thread_start_view),
        name="private-thread-start",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/reply/",
        login_required(
            pgettext_lazy(
                "thread reply login required error",
                "Sign in to reply to threads",
            )
        )(thread_reply_view),
        name="thread-reply",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/reply/",
        login_required(
            pgettext_lazy(
                "thread reply login required error",
                "Sign in to reply to threads",
            )
        )(private_thread_reply_view),
        name="private-thread-reply",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/edit/",
        login_required(
            pgettext_lazy(
                "thread edit login required error",
                "Sign in to edit threads",
            )
        )(thread_edit_view),
        name="thread-edit",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/edit/<int:post_id>/",
        login_required(
            pgettext_lazy(
                "thread post edit login required error",
                "Sign in to edit posts",
            )
        )(thread_post_edit_view),
        name="thread-post-edit",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/edit/",
        login_required(
            pgettext_lazy(
                "thread edit login required error",
                "Sign in to edit threads",
            )
        )(private_thread_edit_view),
        name="private-thread-edit",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/edit/<int:post_id>/",
        login_required(
            pgettext_lazy(
                "thread post edit login required error",
                "Sign in to edit posts",
            )
        )(private_thread_post_edit_view),
        name="private-thread-post-edit",
    ),
]
