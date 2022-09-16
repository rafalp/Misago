from django.urls import path
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
        urlpatterns.namespace("categories/", "categories")

        # Nodes
        urlpatterns.patterns(
            "categories",
            path("", CategoriesList.as_view(), name="index"),
            path("new/", NewCategory.as_view(), name="new"),
            path("edit/<int:pk>/", EditCategory.as_view(), name="edit"),
            path(
                "permissions/<int:pk>/",
                CategoryPermissions.as_view(),
                name="permissions",
            ),
            path("move/down/<int:pk>/", MoveDownCategory.as_view(), name="down"),
            path("move/up/<int:pk>/", MoveUpCategory.as_view(), name="up"),
            path("delete/<int:pk>/", DeleteCategory.as_view(), name="delete"),
        )

        # Category Roles
        urlpatterns.namespace("categories/", "categories", "permissions")
        urlpatterns.patterns(
            "permissions:categories",
            path("", CategoryRolesList.as_view(), name="index"),
            path("new/", NewCategoryRole.as_view(), name="new"),
            path("edit/<int:pk>/", EditCategoryRole.as_view(), name="edit"),
            path("delete/<int:pk>/", DeleteCategoryRole.as_view(), name="delete"),
        )

        # Change Role Category Permissions
        urlpatterns.patterns(
            "permissions",
            path(
                "categories/<int:pk>/",
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
