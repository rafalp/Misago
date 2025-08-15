from django.urls import path

from .views import PrivateThreadMembersAddView


urlpatterns = [
    path(
        "p/<slug:slug>/<int:id>/add-members/",
        PrivateThreadMembersAddView.as_view(),
        name="private-thread-members-add",
    ),
]
