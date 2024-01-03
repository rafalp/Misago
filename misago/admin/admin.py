from django.urls import path
from django.utils.translation import pgettext_lazy

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
            name=pgettext_lazy("admin node", "Moderators"),
            icon="fas fa-shield-alt",
            after="categories:index",
            namespace="moderators",
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
