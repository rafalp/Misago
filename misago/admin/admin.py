from django.conf.urls import url
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _

from .themes.views import (
    ActivateTheme,
    DeleteTheme,
    EditTheme,
    NewTheme,
    ThemeAssets,
    ThemesList,
)


class MisagoAdminExtension(MiddlewareMixin):
    def register_urlpatterns(self, urlpatterns):
        # Appearance section
        urlpatterns.namespace(r"^appearance/", "appearance")

        # Themes
        urlpatterns.namespace(r"^themes/", "themes", "appearance")
        urlpatterns.patterns(
            "appearance:themes",
            url(r"^$", ThemesList.as_view(), name="index"),
            url(r"^new/$", NewTheme.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditTheme.as_view(), name="edit"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteTheme.as_view(), name="delete"),
            url(r"^activate/(?P<pk>\d+)/$", ActivateTheme.as_view(), name="activate"),
            url(r"^assets/(?P<pk>\d+)/$", ThemeAssets.as_view(), name="assets"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Home"),
            icon="fa fa-home",
            parent="misago:admin",
            link="misago:admin:index",
        )

        site.add_node(
            name=_("Appearance"),
            icon="fa fa-paint-brush",
            parent="misago:admin",
            namespace="misago:admin:appearance",
            link="misago:admin:appearance:themes:index",
        )

        site.add_node(
            name=_("Themes"),
            icon="fa fa-tint",
            parent="misago:admin:appearance",
            namespace="misago:admin:appearance:themes",
            link="misago:admin:appearance:themes:index",
        )
