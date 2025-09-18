from django.urls import path

from .views.post import post


urlpatterns = [
    path("post/<int:post_id>/", post, name="post"),
]
