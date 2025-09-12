from django.urls import path

from .views.post import post


urlpatterns = [
    path("post/<int:id>/", post, name="post"),
]
