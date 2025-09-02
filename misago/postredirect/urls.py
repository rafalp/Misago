from django.urls import path

from .views import PostRedirectView


urlpatterns = [
    path(
        "post/<int:id>/",
        PostRedirectView.as_view(),
        name="post",
    ),
]