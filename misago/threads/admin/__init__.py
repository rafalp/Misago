from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views.attachments import AttachmentsList, DeleteAttachment
from .views.attachmenttypes import (
    AttachmentTypesList,
    DeleteAttachmentType,
    EditAttachmentType,
    NewAttachmentType,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Attachment
        urlpatterns.namespace("attachments/", "attachments")
        urlpatterns.patterns(
            "attachments",
            path("", AttachmentsList.as_view(), name="index"),
            path("<int:page>/", AttachmentsList.as_view(), name="index"),
            path("delete/<int:pk>/", DeleteAttachment.as_view(), name="delete"),
        )

        # AttachmentType
        urlpatterns.namespace("attachment-types/", "attachment-types", "settings")
        urlpatterns.patterns(
            "settings:attachment-types",
            path("", AttachmentTypesList.as_view(), name="index"),
            path("new/", NewAttachmentType.as_view(), name="new"),
            path("edit/<int:pk>/", EditAttachmentType.as_view(), name="edit"),
            path("delete/<int:pk>/", DeleteAttachmentType.as_view(), name="delete"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Attachments"),
            icon="fas fa-paperclip",
            after="permissions:index",
            namespace="attachments",
        )

        site.add_node(
            name=_("Attachment types"),
            description=_("Specify what files may be uploaded on the forum."),
            parent="settings",
            namespace="attachment-types",
        )
