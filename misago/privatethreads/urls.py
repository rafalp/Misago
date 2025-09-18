from django.urls import path
from django.utils.translation import pgettext_lazy

from ..auth.decorators import login_required
from .views.detail import PrivateThreadDetailView
from .views.list import PrivateThreadListView
from .views.members import (
    PrivateThreadLeaveView,
    PrivateThreadMemberRemoveView,
    PrivateThreadMembersAddView,
    PrivateThreadOwnerChangeView,
)
from .views.post import (
    PrivateThreadPostLastView,
    PrivateThreadPostUnreadView,
    PrivateThreadPostView,
)


urlpatterns = [
    path(
        "private/",
        login_required(
            pgettext_lazy(
                "private thread login required error",
                "Sign in to view private threads",
            )
        )(PrivateThreadListView.as_view()),
        name="private-thread-list",
    ),
    path(
        "private/<slug:filter>/",
        login_required(
            pgettext_lazy(
                "private thread login required error",
                "Sign in to view private threads",
            )
        )(PrivateThreadListView.as_view()),
        name="private-thread-list",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/",
        login_required(
            pgettext_lazy(
                "private thread login required error",
                "Sign in to view private threads",
            )
        )(PrivateThreadDetailView.as_view()),
        name="private-thread",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/<int:page>/",
        login_required(
            pgettext_lazy(
                "private thread login required error",
                "Sign in to view private threads",
            )
        )(PrivateThreadDetailView.as_view()),
        name="private-thread",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/add-members/",
        PrivateThreadMembersAddView.as_view(),
        name="private-thread-members-add",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/leave/",
        PrivateThreadLeaveView.as_view(),
        name="private-thread-leave",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/change-owner/<int:user_id>/",
        PrivateThreadOwnerChangeView.as_view(),
        name="private-thread-owner-change",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/remove-member/<int:user_id>/",
        PrivateThreadMemberRemoveView.as_view(),
        name="private-thread-member-remove",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/",
        PrivateThreadPostView.as_view(),
        name="private-thread-post",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/last/",
        PrivateThreadPostLastView.as_view(),
        name="private-thread-post-last",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/unread/",
        PrivateThreadPostUnreadView.as_view(),
        name="private-thread-post-unread",
    ),
]
