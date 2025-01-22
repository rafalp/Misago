from django.urls import path
from django.utils.translation import pgettext_lazy

from .attachments import views as attachments
from .categories import views as categories
from .groups import views as groups
from .moderators import views as moderators


class MisagoAdminExtension:
    def register_navigation_nodes(self, site):
        site.add_node(name=pgettext_lazy("admin node", "Dashboard"), icon="fa fa-home")
        site.add_node(
            name=pgettext_lazy("admin node", "Groups"),
            icon="fas fa-adjust",
            after="users:index",
            namespace="groups",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Categories"),
            icon="fas fa-sitemap",
            after="ranks:index",
            namespace="categories",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Moderators"),
            icon="fas fa-shield-alt",
            after="categories:index",
            namespace="moderators",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Attachments"),
            icon="fas fa-paperclip",
            after="permissions:index",
            namespace="attachments",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "File types"),
            parent="attachments",
            namespace="filetypes",
        )

    def register_urlpatterns(self, urlpatterns):
        urlpatterns.namespace("groups/", "groups")
        urlpatterns.patterns(
            "groups",
            path("", groups.ListView.as_view(), name="index"),
            path("ordering/", groups.OrderingView.as_view(), name="ordering"),
            path("new/", groups.NewView.as_view(), name="new"),
            path("edit/<int:pk>/", groups.EditView.as_view(), name="edit"),
            path(
                "categories/<int:pk>/",
                groups.CategoryPermissionsView.as_view(),
                name="categories",
            ),
            path("default/<int:pk>/", groups.MakeDefaultView.as_view(), name="default"),
            path("members/<int:pk>/", groups.MembersView.as_view(), name="members"),
            path(
                "members-main/<int:pk>/",
                groups.MembersMainView.as_view(),
                name="members-main",
            ),
            path("delete/<int:pk>/", groups.DeleteView.as_view(), name="delete"),
        )

        urlpatterns.namespace("categories/", "categories")
        urlpatterns.patterns(
            "categories",
            path("", categories.CategoriesList.as_view(), name="index"),
            path("new/", categories.NewCategory.as_view(), name="new"),
            path("edit/<int:pk>/", categories.EditCategory.as_view(), name="edit"),
            path(
                "permissions/<int:pk>/",
                categories.CategoryPermissionsView.as_view(),
                name="permissions",
            ),
            path(
                "move/down/<int:pk>/",
                categories.MoveDownCategory.as_view(),
                name="down",
            ),
            path("move/up/<int:pk>/", categories.MoveUpCategory.as_view(), name="up"),
            path(
                "delete/<int:pk>/", categories.DeleteCategory.as_view(), name="delete"
            ),
        )

        urlpatterns.namespace("moderators/", "moderators")
        urlpatterns.patterns(
            "moderators",
            path("", moderators.ListView.as_view(), name="index"),
            path(
                "new/group/<int:group>/", moderators.NewView.as_view(), name="new-group"
            ),
            path("new/user/<int:user>/", moderators.NewView.as_view(), name="new-user"),
            path("edit/<int:pk>/", moderators.EditView.as_view(), name="edit"),
            path("delete/<int:pk>/", moderators.DeleteView.as_view(), name="delete"),
        )

        urlpatterns.namespace("attachments/", "attachments")
        urlpatterns.patterns(
            "attachments",
            path("", attachments.AttachmentsList.as_view(), name="index"),
            path("<int:page>/", attachments.AttachmentsList.as_view(), name="index"),
            path(
                "delete/<int:pk>/",
                attachments.DeleteAttachment.as_view(),
                name="delete",
            ),
        )
        urlpatterns.single_pattern(
            "filetypes/",
            "filetypes",
            "attachments",
            attachments.AttachmentsFiletypesList.as_view(),
        )
