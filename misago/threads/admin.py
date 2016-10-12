from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views.admin.attachmenttypes import (
    AttachmentTypesList, DeleteAttachmentType, EditAttachmentType, NewAttachmentType)


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        # AttachmentType
        urlpatterns.namespace(r'^attachment-types/', 'attachment-types', 'system')
        urlpatterns.patterns('system:attachment-types',
            url(r'^$', AttachmentTypesList.as_view(), name='index'),
            url(r'^new/$', NewAttachmentType.as_view(), name='new'),
            url(r'^edit/(?P<pk>\d+)/$', EditAttachmentType.as_view(), name='edit'),
            url(r'^delete/(?P<pk>\d+)/$', DeleteAttachmentType.as_view(), name='delete'),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Attachment types"),
            icon='fa fa-cubes',
            parent='misago:admin:system',
            after='misago:admin:system:settings:index',
            link='misago:admin:system:attachment-types:index'
        )
