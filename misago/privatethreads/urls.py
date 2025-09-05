from django.urls import path

from .views.members import (
    PrivateThreadLeaveView,
    PrivateThreadMemberRemoveView,
    PrivateThreadMembersAddView,
    PrivateThreadOwnerChangeView,
)
from .views.redirect import (
    PrivateThreadLastPostRedirectView,
    PrivateThreadPostRedirectView,
    PrivateThreadUnreadPostRedirectView,
    PrivateThreadUnapprovedPostRedirectView,
)


urlpatterns = [
    path(
        "p/<slug:slug>/<int:id>/add-members/",
        PrivateThreadMembersAddView.as_view(),
        name="private-thread-members-add",
    ),
    path(
        "p/<slug:slug>/<int:id>/leave/",
        PrivateThreadLeaveView.as_view(),
        name="private-thread-leave",
    ),
    path(
        "p/<slug:slug>/<int:id>/change-owner/<int:user_id>/",
        PrivateThreadOwnerChangeView.as_view(),
        name="private-thread-owner-change",
    ),
    path(
        "p/<slug:slug>/<int:id>/remove-member/<int:user_id>/",
        PrivateThreadMemberRemoveView.as_view(),
        name="private-thread-member-remove",
    ),
    path(
        "p/<slug:slug>/<int:id>/post/<int:post_id>/",
        PrivateThreadPostRedirectView.as_view(),
        name="private-thread-post",
    ),
    path(
        "p/<slug:slug>/<int:id>/last/",
        PrivateThreadLastPostRedirectView.as_view(),
        name="private-thread-last-post",
    ),
    path(
        "p/<slug:slug>/<int:id>/unread/",
        PrivateThreadUnreadPostRedirectView.as_view(),
        name="private-thread-unread-post",
    ),
    path(
        "p/<slug:slug>/<int:id>/unapproved/",
        PrivateThreadUnapprovedPostRedirectView.as_view(),
        name="private-thread-unapproved-post",
    ),
]
