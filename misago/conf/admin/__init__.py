from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import index
from .views import (
    ChangeAnalyticsSettingsView,
    ChangeCaptchaSettingsView,
    ChangeGeneralSettingsView,
    ChangeThreadsSettingsView,
    ChangeUsersSettingsView,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.namespace(r"^settings/", "settings")

        urlpatterns.patterns("settings", url(r"^$", index, name="index"))

        urlpatterns.single_pattern(
            r"^analytics/",
            "analytics",
            "settings",
            ChangeAnalyticsSettingsView.as_view(),
        )
        urlpatterns.single_pattern(
            r"^captcha/", "captcha", "settings", ChangeCaptchaSettingsView.as_view()
        )
        urlpatterns.single_pattern(
            r"^general/", "general", "settings", ChangeGeneralSettingsView.as_view()
        )
        urlpatterns.single_pattern(
            r"^threads/", "threads", "settings", ChangeThreadsSettingsView.as_view()
        )
        urlpatterns.single_pattern(
            r"^users/", "users", "settings", ChangeUsersSettingsView.as_view()
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Settings"),
            icon="fa fa-cog",
            after="themes:index",
            namespace="settings",
        )

        site.add_node(
            name=_("General"),
            description=_("Change forum details like name, description or footer."),
            parent="settings",
            namespace="general",
        )
        site.add_node(
            name=_("Users"),
            description=_(
                "Customize user accounts default behavior and features availability."
            ),
            parent="settings",
            namespace="users",
            after="general:index",
        )
        site.add_node(
            name=_("Captcha"),
            description=_(
                "Setup protection against automatic registrations on the site."
            ),
            parent="settings",
            namespace="captcha",
            after="users:index",
        )
        site.add_node(
            name=_("Analytics"),
            description=_("Enable Google Analytics or setup Google Site Verification."),
            parent="settings",
            namespace="analytics",
            after="captcha:index",
        )
        site.add_node(
            name=_("Threads"),
            description=_("Threads, posts, polls and attachments options."),
            parent="settings",
            namespace="threads",
            after="analytics:index",
        )
