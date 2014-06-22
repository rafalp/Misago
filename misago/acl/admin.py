from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from misago.acl.views import RolesList, NewRole, EditRole, DeleteRole


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        # Permissions section
        urlpatterns.namespace(r'^permissions/', 'permissions')

        # Roles
        urlpatterns.namespace(r'^users/', 'users', 'permissions')
        urlpatterns.patterns('permissions:users',
            url(r'^$', RolesList.as_view(), name='index'),
            url(r'^new/$', NewRole.as_view(), name='new'),
            url(r'^edit/(?P<role_id>\d+)/$', EditRole.as_view(), name='edit'),
            url(r'^delete/(?P<role_id>\d+)/$', DeleteRole.as_view(), name='delete'),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            parent='misago:admin',
            after='misago:admin:users:accounts:index',
            namespace='misago:admin:permissions',
            link='misago:admin:permissions:users:index',
            name=_("Permissions"),
            icon='fa fa-adjust')

        site.add_node(
            parent='misago:admin:permissions',
            namespace='misago:admin:permissions:users',
            link='misago:admin:permissions:users:index',
            name=_("User roles"),
            icon='fa fa-th-large')
