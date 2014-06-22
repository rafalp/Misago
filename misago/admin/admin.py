from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from misago.acl.views import RolesList, NewRole, EditRole, DeleteRole


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        pass

    def register_navigation_nodes(self, site):
        site.add_node(
            parent='misago:admin',
            link='misago:admin:index',
            name=_("Home"),
            icon='fa fa-home')
