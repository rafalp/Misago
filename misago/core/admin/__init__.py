from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import ChangeGeneralConfigView


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.single_pattern(
            r"^general/", "general", "settings", ChangeGeneralConfigView.as_view()
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("General"),
            description=_(
                "Those settings control most basic properties "
                "of your forum like its name or description."
            ),
            parent="settings",
            namespace="general",
        )
