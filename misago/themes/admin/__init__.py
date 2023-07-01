from django.urls import path
from django.utils.translation import pgettext_lazy

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
        urlpatterns.namespace("themes/", "themes")
        urlpatterns.patterns(
            "themes",
            path("", ThemesList.as_view(), name="index"),
            path("new/", NewTheme.as_view(), name="new"),
            path("edit/<int:pk>/", EditTheme.as_view(), name="edit"),
            path("delete/<int:pk>/", DeleteTheme.as_view(), name="delete"),
            path("activate/<int:pk>/", ActivateTheme.as_view(), name="activate"),
            path("export/<int:pk>/", ExportTheme.as_view(), name="export"),
            path("import/", ImportTheme.as_view(), name="import"),
            path("assets/<int:pk>/", ThemeAssets.as_view(), name="assets"),
            path(
                "assets/<int:pk>/delete-css/",
                DeleteThemeCss.as_view(),
                name="delete-css",
            ),
            path(
                "assets/<int:pk>/delete-media/",
                DeleteThemeMedia.as_view(),
                name="delete-media",
            ),
            path(
                "assets/<int:pk>/upload-css/",
                UploadThemeCss.as_view(),
                name="upload-css",
            ),
            path(
                "assets/<int:pk>/upload-media/",
                UploadThemeMedia.as_view(),
                name="upload-media",
            ),
            path(
                "assets/<int:pk>/move-css-down/<int:css_pk>/",
                MoveThemeCssDown.as_view(),
                name="move-css-down",
            ),
            path(
                "assets/<int:pk>/move-css-up/<int:css_pk>/",
                MoveThemeCssUp.as_view(),
                name="move-css-up",
            ),
            path(
                "assets/<int:pk>/new-css/",
                NewThemeCss.as_view(),
                name="new-css-file",
            ),
            path(
                "assets/<int:pk>/edit-css/<int:css_pk>/",
                EditThemeCss.as_view(),
                name="edit-css-file",
            ),
            path(
                "assets/<int:pk>/new-css-link/",
                NewThemeCssLink.as_view(),
                name="new-css-link",
            ),
            path(
                "assets/<int:pk>/edit-css-link/<int:css_pk>/",
                EditThemeCssLink.as_view(),
                name="edit-css-link",
            ),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=pgettext_lazy("admin node", "Themes"),
            icon="fa fa-paint-brush",
            after="attachments:index",
            namespace="themes",
        )
