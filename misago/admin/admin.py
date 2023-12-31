from django.urls import path
from django.utils.translation import pgettext_lazy

from .moderators import views as moderators


class MisagoAdminExtension:
    def register_navigation_nodes(self, site):
        site.add_node(name=pgettext_lazy("admin node", "Dashboard"), icon="fa fa-home")
        site.add_node(
            name=pgettext_lazy("admin node", "Moderators"),
            icon="fas fa-shield-alt",
            after="categories:index",
            namespace="moderators",
        )

    def register_urlpatterns(self, urlpatterns):
        # Moderators
        urlpatterns.namespace("moderators/", "moderators")
        urlpatterns.patterns(
            "moderators",
            path("", moderators.ListView.as_view(), name="index"),
        )
