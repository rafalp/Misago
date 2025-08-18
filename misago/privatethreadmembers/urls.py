from django.urls import path

from .views import (
    PrivateThreadMembersAddView,
    PrivateThreadMemberRemoveView,
    PrivateThreadOwnerChangeView,
)


urlpatterns = [
    path(
        "p/<slug:slug>/<int:id>/add-members/",
        PrivateThreadMembersAddView.as_view(),
        name="private-thread-members-add",
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
]
