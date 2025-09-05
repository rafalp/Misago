from django.urls import path

from .views.redirect import PostView


urlpatterns = [
    path(
        "post/<int:id>/",
        PostView.as_view(),
        name="post",
    ),
]
