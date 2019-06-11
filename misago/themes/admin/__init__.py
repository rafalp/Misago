from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import (
    ActivateTheme,
    DeleteTheme,
    DeleteThemeCss,
    DeleteThemeMedia,
    EditTheme,
    EditThemeCss,
    EditThemeCssLink,
    MoveThemeCssDown,
    MoveThemeCssUp,
    NewTheme,
    NewThemeCss,
    NewThemeCssLink,
    ExportTheme,
    ImportTheme,
    ThemeAssets,
    ThemesList,
    UploadThemeCss,
    UploadThemeMedia,
)


class MisagoAdminExtension:
    def register_urlpatterns(self, urlpatterns):
        # Themes
        urlpatterns.namespace(r"^themes/", "themes")
        urlpatterns.patterns(
            "themes",
            url(r"^$", ThemesList.as_view(), name="index"),
            url(r"^new/$", NewTheme.as_view(), name="new"),
            url(r"^edit/(?P<pk>\d+)/$", EditTheme.as_view(), name="edit"),
            url(r"^delete/(?P<pk>\d+)/$", DeleteTheme.as_view(), name="delete"),
            url(r"^activate/(?P<pk>\d+)/$", ActivateTheme.as_view(), name="activate"),
            url(r"^export/(?P<pk>\d+)/$", ExportTheme.as_view(), name="export"),
            url(r"^import/$", ImportTheme.as_view(), name="import"),
            url(r"^assets/(?P<pk>\d+)/$", ThemeAssets.as_view(), name="assets"),
            url(
                r"^assets/(?P<pk>\d+)/delete-css/$",
                DeleteThemeCss.as_view(),
                name="delete-css",
            ),
            url(
                r"^assets/(?P<pk>\d+)/delete-media/$",
                DeleteThemeMedia.as_view(),
                name="delete-media",
            ),
            url(
                r"^assets/(?P<pk>\d+)/upload-css/$",
                UploadThemeCss.as_view(),
                name="upload-css",
            ),
            url(
                r"^assets/(?P<pk>\d+)/upload-media/$",
                UploadThemeMedia.as_view(),
                name="upload-media",
            ),
            url(
                r"^assets/(?P<pk>\d+)/move-css-down/(?P<css_pk>\d+)/$",
                MoveThemeCssDown.as_view(),
                name="move-css-down",
            ),
            url(
                r"^assets/(?P<pk>\d+)/move-css-up/(?P<css_pk>\d+)/$",
                MoveThemeCssUp.as_view(),
                name="move-css-up",
            ),
            url(
                r"^assets/(?P<pk>\d+)/new-css/$",
                NewThemeCss.as_view(),
                name="new-css-file",
            ),
            url(
                r"^assets/(?P<pk>\d+)/edit-css/(?P<css_pk>\d+)/$",
                EditThemeCss.as_view(),
                name="edit-css-file",
            ),
            url(
                r"^assets/(?P<pk>\d+)/new-css-link/$",
                NewThemeCssLink.as_view(),
                name="new-css-link",
            ),
            url(
                r"^assets/(?P<pk>\d+)/edit-css-link/(?P<css_pk>\d+)/$",
                EditThemeCssLink.as_view(),
                name="edit-css-link",
            ),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Themes"),
            icon="fa fa-paint-brush",
            after="attachments:index",
            namespace="themes",
        )
