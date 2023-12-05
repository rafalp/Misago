from django.urls import path
from django.utils.translation import pgettext_lazy

from .views import plugins_list


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.namespace("plugins/", "plugins")

        urlpatterns.patterns("plugins", path("", plugins_list, name="index"))

    def register_navigation_nodes(self, site):
        site.add_node(
            name=pgettext_lazy("admin node", "Plugins"),
            icon="fa fa-cube",
            after="settings:index",
            namespace="plugins",
        )
