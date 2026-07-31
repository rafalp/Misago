from django.urls import path

from ..plugins import extensions
from .decorators import private_threads_login_required
from .views import (
    PrivateThreadDetailView,
    PrivateThreadLeaveView,
    PrivateThreadListView,
    PrivateThreadMemberRemoveView,
    PrivateThreadMembersAddView,
    PrivateThreadOwnerChangeView,
    PrivateThreadPostLastView,
    PrivateThreadPostUnapprovedView,
    PrivateThreadPostUnreadView,
    PrivateThreadPostView,
)

private_thread_list_view = extensions.get(PrivateThreadListView).as_view()
private_thread_detail_view = extensions.get(PrivateThreadDetailView).as_view()
private_thread_members_add_view = extensions.get(PrivateThreadMembersAddView).as_view()
private_thread_leave_view = extensions.get(PrivateThreadLeaveView).as_view()
private_thread_owner_change_view = extensions.get(
    PrivateThreadOwnerChangeView
).as_view()
private_thread_member_remove_view = extensions.get(
    PrivateThreadMemberRemoveView
).as_view()
private_thread_post_view = extensions.get(PrivateThreadPostView).as_view()
private_thread_post_last_view = extensions.get(PrivateThreadPostLastView).as_view()
private_thread_post_unapproved_view = extensions.get(
    PrivateThreadPostUnapprovedView
).as_view()
private_thread_post_unread_view = extensions.get(PrivateThreadPostUnreadView).as_view()

urlpatterns = [
    path(
        "private/",
        private_threads_login_required(private_thread_list_view),
        name="private-thread-list",
    ),
    path(
        "private/<slug:filter>/",
        private_threads_login_required(private_thread_list_view),
        name="private-thread-list",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/",
        private_threads_login_required(private_thread_detail_view),
        name="private-thread",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/<int:page>/",
        private_threads_login_required(private_thread_detail_view),
        name="private-thread",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/add-members/",
        private_thread_members_add_view,
        name="private-thread-members-add",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/leave/",
        private_thread_leave_view,
        name="private-thread-leave",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/change-owner/<int:user_id>/",
        private_thread_owner_change_view,
        name="private-thread-owner-change",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/remove-member/<int:user_id>/",
        private_thread_member_remove_view,
        name="private-thread-member-remove",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/",
        private_thread_post_view,
        name="private-thread-post",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/last/",
        private_thread_post_last_view,
        name="private-thread-post-last",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/unapproved/",
        private_thread_post_unapproved_view,
        name="private-thread-post-unapproved",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/unread/",
        private_thread_post_unread_view,
        name="private-thread-post-unread",
    ),
]
