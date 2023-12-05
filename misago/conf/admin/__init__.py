from django.urls import path
from django.utils.translation import pgettext_lazy

from .views import (
    AnalyticsSettingsView,
    CaptchaSettingsView,
    GeneralSettingsView,
    NotificationsSettingsView,
    OAuth2SettingsView,
    ThreadsSettingsView,
    UsersSettingsView,
    index,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.namespace("settings/", "settings")

        urlpatterns.patterns("settings", path("", index, name="index"))

        urlpatterns.single_pattern(
            "analytics/",
            "analytics",
            "settings",
            AnalyticsSettingsView.as_view(),
        )
        urlpatterns.single_pattern(
            "captcha/", "captcha", "settings", CaptchaSettingsView.as_view()
        )
        urlpatterns.single_pattern(
            "general/", "general", "settings", GeneralSettingsView.as_view()
        )
        urlpatterns.single_pattern(
            "notifications/",
            "notifications",
            "settings",
            NotificationsSettingsView.as_view(),
        )
        urlpatterns.single_pattern(
            "oauth2/", "oauth2", "settings", OAuth2SettingsView.as_view()
        )
        urlpatterns.single_pattern(
            "threads/", "threads", "settings", ThreadsSettingsView.as_view()
        )
        urlpatterns.single_pattern(
            "users/", "users", "settings", UsersSettingsView.as_view()
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=pgettext_lazy("admin node", "Settings"),
            icon="fa fa-cog",
            after="themes:index",
            namespace="settings",
        )

        site.add_node(
            name=pgettext_lazy("admin node", "General"),
            description=pgettext_lazy(
                "admin node", "Change forum details like name, description or footer."
            ),
            parent="settings",
            namespace="general",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Users"),
            description=pgettext_lazy(
                "admin node",
                "Customize user accounts default behavior and features availability.",
            ),
            parent="settings",
            namespace="users",
            after="general:index",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Captcha"),
            description=pgettext_lazy(
                "admin node",
                "Setup protection against automatic registrations on the site.",
            ),
            parent="settings",
            namespace="captcha",
            after="users:index",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Threads"),
            description=pgettext_lazy(
                "admin node", "Threads, posts, polls and attachments options."
            ),
            parent="settings",
            namespace="threads",
            after="captcha:index",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Notifications"),
            description=pgettext_lazy(
                "admin node",
                "Those settings control default notification preferences of new user accounts and storage time of existing notifications.",
            ),
            parent="settings",
            namespace="notifications",
            after="threads:index",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "OAuth2"),
            description=pgettext_lazy(
                "admin node",
                "Enable OAuth2 client and connect your site to existing auth provider.",
            ),
            parent="settings",
            namespace="oauth2",
            after="notifications:index",
        )
        site.add_node(
            name=pgettext_lazy("admin node", "Analytics"),
            description=pgettext_lazy(
                "admin node",
                "Enable Google Analytics or setup Google Site Verification.",
            ),
            parent="settings",
            namespace="analytics",
            after="oauth2:index",
        )
