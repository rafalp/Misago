from django.urls import path

from .views import attachment_details, attachment_download, attachment_thumbnail


urlpatterns = [
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
        "a/<slug:slug>/<int:id>/thumbnail/",
        attachment_thumbnail,
        name="attachment-thumbnail",
    ),
]
