from django.urls import path

from .views import attachment_download, attachment_thumbnail


urlpatterns = [
    path(
        "a/<filename>/<int:id>/",
        attachment_download,
        name="attachment-download",
    ),
    path(
        "a/<filename>/<int:id>/thumbnail/",
        attachment_thumbnail,
        name="attachment-thumbnail",
    ),
]
