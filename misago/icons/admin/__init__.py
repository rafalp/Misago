from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import icons_admin


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Icons
        urlpatterns.namespace(r"^icons/", "icons", "settings")
        urlpatterns.patterns("settings:icons", url(r"^$", icons_admin, name="index"))

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Icons"),
            description=_("Upload favicon and application icon for the site."),
            parent="settings",
            namespace="icons",
        )
