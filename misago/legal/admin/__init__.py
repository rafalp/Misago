from django.urls import path
from django.utils.translation import pgettext_lazy

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
        urlpatterns.namespace("agreements/", "agreements", "settings")
        urlpatterns.patterns(
            "settings:agreements",
            path("", AgreementsList.as_view(), name="index"),
            path("<int:page>/", AgreementsList.as_view(), name="index"),
            path("new/", NewAgreement.as_view(), name="new"),
            path("edit/<int:pk>/", EditAgreement.as_view(), name="edit"),
            path("delete/<int:pk>/", DeleteAgreement.as_view(), name="delete"),
            path(
                "set-as-active/<int:pk>/",
                SetAgreementAsActive.as_view(),
                name="set-as-active",
            ),
            path("disable/<int:pk>/", DisableAgreement.as_view(), name="disable"),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=pgettext_lazy("admin node", "Legal agreements"),
            description=pgettext_lazy(
                "admin node", "Set terms of service and privacy policy contents."
            ),
            parent="settings",
            namespace="agreements",
        )
