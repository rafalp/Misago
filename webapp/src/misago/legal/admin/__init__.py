from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import (
    AgreementsList,
    DeleteAgreement,
    DisableAgreement,
    EditAgreement,
    NewAgreement,
    SetAgreementAsActive,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Legal Agreements
        urlpatterns.namespace(r"^agreements/", "agreements", "settings")
        urlpatterns.patterns(
            "settings:agreements",
            url(r"^$", AgreementsList.as_view(), name="index"),
            url(r"^(?P<page>\d+)/$", AgreementsList.as_view(), name="index"),
            url(r"^new/$", NewAgreement.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditAgreement.as_view(), name="edit"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteAgreement.as_view(), name="delete"),
            url(
                r"^set-as-active/(?P<pk>\d+)/$",
                SetAgreementAsActive.as_view(),
                name="set-as-active",
            ),
            url(r"^disable/(?P<pk>\d+)/$", DisableAgreement.as_view(), name="disable"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Legal agreements"),
            description=_("Set terms of service and privacy policy contents."),
            parent="settings",
            namespace="agreements",
        )
