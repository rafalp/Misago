from django.conf.urls import url
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
        urlpatterns.namespace(r"^attachments/", "attachments")
        urlpatterns.patterns(
            "attachments",
            url(r"^$", AttachmentsList.as_view(), name="index"),
            url(r"^(?P<page>\d+)/$", AttachmentsList.as_view(), name="index"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteAttachment.as_view(), name="delete"),
        )

        # AttachmentType
        urlpatterns.namespace(r"^attachment-types/", "attachment-types", "settings")
        urlpatterns.patterns(
            "settings:attachment-types",
            url(r"^$", AttachmentTypesList.as_view(), name="index"),
            url(r"^new/$", NewAttachmentType.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditAttachmentType.as_view(), name="edit"),
            url(
                r"^delete/(?P<pk>\d+)/$", DeleteAttachmentType.as_view(), name="delete"
            ),
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
