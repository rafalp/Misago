from django.conf.urls import url
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
            url(r"^$", MenuItemsList.as_view(), name="index"),
            url(r"^(?P<page>\d+)/$", MenuItemsList.as_view(), name="index"),
            url(r"^new/$", NewMenuItem.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditMenuItem.as_view(), name="edit"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteMenuItem.as_view(), name="delete"),
            url(r"^down/(?P<pk>(\w|-)+)/$", MoveDownMenuItem.as_view(), name="down"),
            url(r"^up/(?P<pk>(\w|-)+)/$", MoveUpMenuItem.as_view(), name="up"),
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
