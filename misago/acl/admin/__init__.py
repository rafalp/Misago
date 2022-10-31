from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import DeleteRole, EditRole, NewRole, RolesList, RoleUsers


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Permissions section
        urlpatterns.namespace("permissions/", "permissions")

        # Roles
        urlpatterns.patterns(
            "permissions",
            path("", RolesList.as_view(), name="index"),
            path("new/", NewRole.as_view(), name="new"),
            path("edit/<int:pk>/", EditRole.as_view(), name="edit"),
            path("users/<int:pk>/", RoleUsers.as_view(), name="users"),
            path("delete/<int:pk>/", DeleteRole.as_view(), name="delete"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Permissions"),
            icon="fa fa-adjust",
            after="categories:index",
            namespace="permissions",
        )
