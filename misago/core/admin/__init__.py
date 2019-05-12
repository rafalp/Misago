from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import ChangeGeneralSettingsView


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.single_pattern(
            r"^general/", "general", "settings", ChangeGeneralSettingsView.as_view()
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("General"),
            description=_(
                "Change forum details like name, description or footer."
            ),
            parent="settings",
            namespace="general",
        )
