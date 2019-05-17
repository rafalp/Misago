import os

import pytest
from django.urls import reverse

from ....test import assert_contains
from ...models import Theme

import_link = reverse("misago:admin:themes:import")


class MockThemeExport:
    def __init__(self, response):
        self.name = "theme-export.zip"
        self.content_type = response["content-type"]
        self.size = response["content-length"]
        self._response = response

    def read(self):
        return self._response.getvalue()


@pytest.fixture
def reimport_theme(admin_client):
    def export_import_theme(theme, extra_data=None):
        export_link = reverse("misago:admin:themes:export", kwargs={"pk": theme.pk})
        theme_export = MockThemeExport(admin_client.post(export_link))

        data = extra_data or {}
        data["upload"] = theme_export
        admin_client.post(import_link, data)

        return Theme.objects.filter(pk__gt=theme.pk).last()

    return export_import_theme


def assert_filenames_are_same(src, dst):
    source_filename = os.path.split(src.path)[-1]
    imported_filename = os.path.split(dst.path)[-1]
    assert source_filename == imported_filename


def test_import_theme_form_is_displayed(admin_client):
    response = admin_client.get(import_link)
    assert_contains(response, "Import theme")


def test_theme_import_fails_if_export_was_not_uploaded(admin_client):
    admin_client.post(import_link, {"upload": ""})
    assert Theme.objects.count() == 1


def test_empty_theme_export_can_be_imported_back(reimport_theme, theme):
    assert reimport_theme(theme)


def test_theme_can_be_imported_with_custom_name(reimport_theme, theme):
    imported_theme = reimport_theme(theme, {"name": "Imported theme"})
    assert imported_theme.name == "Imported theme"


def test_theme_can_be_imported_without_parent(reimport_theme, theme):
    imported_theme = reimport_theme(theme)
    assert imported_theme.parent is None


def test_theme_can_be_imported_with_custom_parent(reimport_theme, theme):
    imported_theme = reimport_theme(theme, {"parent": theme.pk})
    assert imported_theme.parent == theme


def test_theme_can_be_imported_with_default_theme_asparent(
    reimport_theme, theme, default_theme
):
    imported_theme = reimport_theme(theme, {"parent": default_theme.pk})
    assert imported_theme.parent == default_theme


def test_theme_import_fails_if_parent_is_nonexisisting(
    reimport_theme, theme, nonexisting_theme
):
    assert not reimport_theme(theme, {"parent": nonexisting_theme.pk})


def test_importing_theme_under_parent_rebuilds_themes_tree(reimport_theme, theme):
    imported_theme = reimport_theme(theme, {"parent": theme.pk})
    theme.refresh_from_db()

    assert imported_theme.tree_id == theme.tree_id
    assert theme.lft == 1
    assert theme.rght == 4
    assert imported_theme.lft == 2
    assert imported_theme.rght == 3


def test_theme_details_are_exported_and_imported_back(reimport_theme, theme):
    theme.name = "Exported Theme"
    theme.version = "0.1.2 FINAL"
    theme.author = "John Doe"
    theme.url = "https://example.com"
    theme.save()

    imported_theme = reimport_theme(theme)

    assert imported_theme.name == theme.name
    assert imported_theme.version == theme.version
    assert imported_theme.author == theme.author
    assert imported_theme.url == theme.url


def test_imported_theme_has_own_dirname(reimport_theme, theme):
    imported_theme = reimport_theme(theme)
    assert theme.dirname != imported_theme.dirname


def test_css_file_is_exported_and_imported_back(reimport_theme, theme, css):
    imported_theme = reimport_theme(theme)

    imported_css = imported_theme.css.last()
    assert imported_css.name == css.name
    assert imported_css.source_hash == css.source_hash
    assert imported_css.size == css.size

    assert_filenames_are_same(css.source_file, imported_css.source_file)


def test_css_link_is_exported_and_imported_back(reimport_theme, theme, css_link):
    imported_theme = reimport_theme(theme)

    imported_css = imported_theme.css.last()
    assert imported_css.name == css_link.name
    assert imported_css.url == css_link.url


def test_importing_css_link_triggers_getting_remote_css_size_task(
    reimport_theme, theme, css_link, mock_update_remote_css_size
):
    reimport_theme(theme)
    mock_update_remote_css_size.assert_called_once()


def test_theme_export_containing_css_file_and_link_can_be_imported_back(
    reimport_theme, theme, css, css_link
):
    imported_theme = reimport_theme(theme)
    css_names = list(imported_theme.css.values_list("name", flat=True))
    assert css_names == [css.name, css_link.name]


def test_theme_css_order_is_preserved_after_import(
    reimport_theme, theme, css, css_link
):
    css_link.order = 1
    css_link.save()

    css.order = 2
    css.save()

    imported_theme = reimport_theme(theme)
    css_names = list(imported_theme.css.values_list("name", flat=True))
    assert css_names == [css_link.name, css.name]


def test_theme_export_containing_media_file_can_be_imported_back(
    reimport_theme, theme, media
):
    imported_theme = reimport_theme(theme)

    imported_media = imported_theme.media.last()
    assert imported_media.name == media.name
    assert imported_media.hash == media.hash
    assert imported_media.type == media.type
    assert imported_media.size == media.size

    assert_filenames_are_same(media.file, imported_media.file)


def test_theme_export_containing_image_file_can_be_imported_back(
    reimport_theme, theme, image
):
    imported_theme = reimport_theme(theme)

    imported_image = imported_theme.media.last()
    assert imported_image.name == image.name
    assert imported_image.hash == image.hash
    assert imported_image.type == image.type
    assert imported_image.width == image.width
    assert imported_image.height == image.height
    assert imported_image.size == image.size

    assert_filenames_are_same(image.file, imported_image.file)


def test_theme_export_containing_different_files_can_be_imported_back(
    reimport_theme, theme, css, css_link, media, image
):
    imported_theme = reimport_theme(theme)

    css_names = list(imported_theme.css.values_list("name", flat=True))
    assert css_names == [css.name, css_link.name]

    media_names = list(imported_theme.media.values_list("name", flat=True))
    assert media_names == [image.name, media.name]


def test_importing_theme_triggers_css_build(
    reimport_theme, theme, css_link, mock_build_theme_css
):
    imported_theme = reimport_theme(theme)
    mock_build_theme_css.assert_called_once_with(imported_theme.pk)
