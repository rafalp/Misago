from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views.categories import (
    CategoriesList,
    DeleteCategory,
    EditCategory,
    MoveDownCategory,
    MoveUpCategory,
    NewCategory,
)
from .views.perms import (
    CategoryPermissions,
    CategoryRolesList,
    DeleteCategoryRole,
    EditCategoryRole,
    NewCategoryRole,
    RoleCategoriesACL,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Categories section
        urlpatterns.namespace(r"^categories/", "categories")

        # Nodes
        urlpatterns.patterns(
            "categories",
            url(r"^$", CategoriesList.as_view(), name="index"),
            url(r"^new/$", NewCategory.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditCategory.as_view(), name="edit"),
            url(
                r"^permissions/(?P<pk>\d+)/$",
                CategoryPermissions.as_view(),
                name="permissions",
            ),
            url(r"^move/down/(?P<pk>\d+)/$", MoveDownCategory.as_view(), name="down"),
            url(r"^move/up/(?P<pk>\d+)/$", MoveUpCategory.as_view(), name="up"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteCategory.as_view(), name="delete"),
        )

        # Category Roles
        urlpatterns.namespace(r"^categories/", "categories", "permissions")
        urlpatterns.patterns(
            "permissions:categories",
            url(r"^$", CategoryRolesList.as_view(), name="index"),
            url(r"^new/$", NewCategoryRole.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditCategoryRole.as_view(), name="edit"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteCategoryRole.as_view(), name="delete"),
        )

        # Change Role Category Permissions
        urlpatterns.patterns(
            "permissions",
            url(
                r"^categories/(?P<pk>\d+)/$",
                RoleCategoriesACL.as_view(),
                name="categories",
            ),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Categories"),
            icon="fas fa-sitemap",
            after="ranks:index",
            namespace="categories",
        )

        site.add_node(
            name=_("Category permissions"), parent="permissions", namespace="categories"
        )
