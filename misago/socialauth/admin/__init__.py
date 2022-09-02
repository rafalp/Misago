from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _

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
        urlpatterns.namespace(r"^social-auth/", "socialauth", "settings")
        urlpatterns.patterns(
            "settings:socialauth",
            path("", SocialAuthProvidersList.as_view(), name="index"),
            re_path(
                "edit/(?P<pk>(\w|-)+)/$",
                EditSocialAuthProvider.as_view(),
                name="edit",
            ),
            re_path(
                "down/(?P<pk>(\w|-)+)/$",
                MoveDownSocialAuthProvider.as_view(),
                name="down",
            ),
            re_path(
                "up/(?P<pk>(\w|-)+)/$", MoveUpSocialAuthProvider.as_view(), name="up"
            ),
            re_path(
                "disable/(?P<pk>(\w|-)+)/$",
                DisableSocialAuthProvider.as_view(),
                name="disable",
            ),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Social login"),
            description=_(
                "Enable users to sign on and login using their social profile."
            ),
            parent="settings",
            namespace="socialauth",
        )
