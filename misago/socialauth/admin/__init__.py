from django.urls import path
from django.utils.translation import pgettext_lazy

from .views import (
    DisableSocialAuthProvider,
    EditSocialAuthProvider,
    MoveDownSocialAuthProvider,
    MoveUpSocialAuthProvider,
    SocialAuthProvidersList,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Social auth providers
        urlpatterns.namespace("social-auth/", "socialauth", "settings")
        urlpatterns.patterns(
            "settings:socialauth",
            path("", SocialAuthProvidersList.as_view(), name="index"),
            path(
                "edit/<slug:pk>/",
                EditSocialAuthProvider.as_view(),
                name="edit",
            ),
            path(
                "down/<slug:pk>/",
                MoveDownSocialAuthProvider.as_view(),
                name="down",
            ),
            path("up/<slug:pk>/", MoveUpSocialAuthProvider.as_view(), name="up"),
            path(
                "disable/<slug:pk>/",
                DisableSocialAuthProvider.as_view(),
                name="disable",
            ),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=pgettext_lazy("admin node", "Social login"),
            description=pgettext_lazy(
                "admin node",
                "Enable users to sign on and login using their social profile.",
            ),
            parent="settings",
            namespace="socialauth",
        )
