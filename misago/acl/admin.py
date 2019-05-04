from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import DeleteRole, EditRole, NewRole, RolesList, RoleUsers


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Permissions section
        urlpatterns.namespace(r"^permissions/", "permissions")

        # Roles
        urlpatterns.patterns(
            "permissions",
            url(r"^$", RolesList.as_view(), name="index"),
            url(r"^new/$", NewRole.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditRole.as_view(), name="edit"),
            url(r"^users/(?P<pk>\d+)/$", RoleUsers.as_view(), name="users"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteRole.as_view(), name="delete"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Permissions"),
            icon="fa fa-adjust",
            after="categories:index",
            namespace="permissions",
        )
