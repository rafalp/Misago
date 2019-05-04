from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from . import views


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.namespace(r"^settings/", "settings")

        urlpatterns.patterns(
            "settings",
            url(r"^$", views.index, name="index"),
            url(r"^group/(?P<key>(\w|-)+)/$", views.group, name="group"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Settings"),
            icon="fa fa-cog",
            after="themes:index",
            namespace="settings",
        )
