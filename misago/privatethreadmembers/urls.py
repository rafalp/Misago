from django.urls import path

from .views import PrivateThreadAddMembersView


urlpatterns = [
    path(
        "p/<slug:slug>/<int:id>/add-members/",
        PrivateThreadAddMembersView.as_view(),
        name="private-thread-add-members",
    ),
]
