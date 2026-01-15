from django.urls import path

from .decorators import private_threads_login_required
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
        private_threads_login_required(PrivateThreadListView.as_view()),
        name="private-thread-list",
    ),
    path(
        "private/<slug:filter>/",
        private_threads_login_required(PrivateThreadListView.as_view()),
        name="private-thread-list",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/",
        private_threads_login_required(PrivateThreadDetailView.as_view()),
        name="private-thread",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/<int:page>/",
        private_threads_login_required(PrivateThreadDetailView.as_view()),
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
