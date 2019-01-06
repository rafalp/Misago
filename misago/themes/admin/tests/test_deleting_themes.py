from pathlib import Path

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse

from ....test import assert_has_error_message
from ...models import Theme, Css, Media


@pytest.fixture
def delete_link(theme):
    return reverse("misago:admin:appearance:themes:delete", kwargs={"pk": theme.pk})


def test_theme_without_children_can_be_deleted(admin_client, delete_link, theme):
    admin_client.post(delete_link)
    with pytest.raises(Theme.DoesNotExist):
        theme.refresh_from_db()


def test_theme_css_are_deleted_together_with_theme(admin_client, delete_link, css):
    admin_client.post(delete_link)
    with pytest.raises(Css.DoesNotExist):
        css.refresh_from_db()


def test_theme_source_css_files_are_deleted_together_with_theme(
    admin_client, delete_link, css
):
    admin_client.post(delete_link)
    assert not Path(css.source_file.path).exists()


def test_theme_build_css_files_are_deleted_together_with_theme(
    admin_client, delete_link, css
):
    css.build_file = ContentFile("body {}", name="test.css")
    css.build_hash = "abcdefgh"
    css.save()

    admin_client.post(delete_link)
    assert not Path(css.build_file.path).exists()


def test_theme_media_are_deleted_together_with_theme(admin_client, delete_link, media):
    admin_client.post(delete_link)
    with pytest.raises(Media.DoesNotExist):
        media.refresh_from_db()


def test_theme_media_files_are_deleted_together_with_theme(
    admin_client, delete_link, media
):
    admin_client.post(delete_link)
    assert not Path(media.file.path).exists()


def test_deleting_default_theme_sets_error_message(admin_client, default_theme):
    delete_link = reverse(
        "misago:admin:appearance:themes:delete", kwargs={"pk": default_theme.pk}
    )
    response = admin_client.post(delete_link)
    assert_has_error_message(response)


def test_default_theme_is_not_deleted(admin_client, default_theme):
    delete_link = reverse(
        "misago:admin:appearance:themes:delete", kwargs={"pk": default_theme.pk}
    )
    response = admin_client.post(delete_link)
    default_theme.refresh_from_db()


def test_deleting_active_theme_sets_error_message(admin_client, theme):
    theme.is_active = True
    theme.save()

    delete_link = reverse(
        "misago:admin:appearance:themes:delete", kwargs={"pk": theme.pk}
    )
    response = admin_client.post(delete_link)
    assert_has_error_message(response)


def test_active_theme_is_not_deleted(admin_client, theme):
    theme.is_active = True
    theme.save()

    delete_link = reverse(
        "misago:admin:appearance:themes:delete", kwargs={"pk": theme.pk}
    )
    admin_client.post(delete_link)
    theme.refresh_from_db()
