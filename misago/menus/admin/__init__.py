from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import (
    DeleteMenuLink,
    EditMenuLink,
    MenuLinksList,
    MoveDownMenuLink,
    MoveUpMenuLink,
    NewMenuLink,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Menu links
        urlpatterns.namespace(r"^links/", "links", "settings")
        urlpatterns.patterns(
            "settings:links",
            url(r"^$", MenuLinksList.as_view(), name="index"),
            url(r"^(?P<page>\d+)/$", MenuLinksList.as_view(), name="index"),
            url(r"^new/$", NewMenuLink.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditMenuLink.as_view(), name="edit"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteMenuLink.as_view(), name="delete"),
            url(r"^down/(?P<pk>(\w|-)+)/$", MoveDownMenuLink.as_view(), name="down"),
            url(r"^up/(?P<pk>(\w|-)+)/$", MoveUpMenuLink.as_view(), name="up"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Menu links"),
            description=_("Add custom links to navbar and footer menus."),
            parent="settings",
            namespace="links",
        )
