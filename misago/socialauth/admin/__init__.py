from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import SocialAuthProvidersList, EditSocialAuthProvider


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Social auth providers
        urlpatterns.namespace(r"^social-auth/", "socialauth", "settings")
        urlpatterns.patterns(
            "settings:socialauth",
            url(r"^$", SocialAuthProvidersList.as_view(), name="index"),
            url(r"^edit/(?P<pk>\w+)/$", EditSocialAuthProvider.as_view(), name="edit"),
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
