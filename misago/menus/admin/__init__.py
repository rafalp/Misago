from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _

from .views import (
    DeleteMenuItem,
    EditMenuItem,
    MenuItemsList,
    MoveDownMenuItem,
    MoveUpMenuItem,
    NewMenuItem,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Menu items
        urlpatterns.namespace(r"^menu-items/", "menu-items", "settings")
        urlpatterns.patterns(
            "settings:menu-items",
            path("", MenuItemsList.as_view(), name="index"),
            path("<int:page>/", MenuItemsList.as_view(), name="index"),
            path("new/", NewMenuItem.as_view(), name="new"),
            path("edit/<int:pk>/", EditMenuItem.as_view(), name="edit"),
            path("delete/<int:pk>/", DeleteMenuItem.as_view(), name="delete"),
            re_path("down/(?P<pk>(\w|-)+)/$", MoveDownMenuItem.as_view(), name="down"),
            re_path("up/(?P<pk>(\w|-)+)/$", MoveUpMenuItem.as_view(), name="up"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Menu items"),
            description=_(
                "Use those options to add custom items to the navbar and footer menus."
            ),
            parent="settings",
            namespace="menu-items",
        )
