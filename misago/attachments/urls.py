from django.urls import path

from .views import (
    attachment_delete,
    attachment_details,
    attachment_download,
    attachment_thumbnail,
    attachments_upload,
)


urlpatterns = [
    path(
        "a/upload/",
        attachments_upload,
        name="attachments-upload",
    ),
    path(
        "a/<slug:slug>/<int:id>/",
        attachment_download,
        name="attachment-download",
    ),
    path(
        "a/<slug:slug>/<int:id>/details/",
        attachment_details,
        name="attachment-details",
    ),
    path(
        "a/<slug:slug>/<int:id>/delete/",
        attachment_delete,
        name="attachment-delete",
    ),
    path(
        "a/<slug:slug>/<int:id>/thumbnail/",
        attachment_thumbnail,
        name="attachment-thumbnail",
    ),
]
