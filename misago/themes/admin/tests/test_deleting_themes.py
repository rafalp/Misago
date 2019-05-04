from pathlib import Path

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ....test import assert_has_error_message
from ... import THEME_CACHE
from ...models import Theme, Css, Media


@pytest.fixture
def delete_link(theme):
    return reverse("misago:admin:themes:delete", kwargs={"pk": theme.pk})


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


def test_theme_images_are_deleted_together_with_theme(admin_client, delete_link, image):
    admin_client.post(delete_link)
    with pytest.raises(Media.DoesNotExist):
        image.refresh_from_db()


def test_theme_media_files_are_deleted_together_with_theme(
    admin_client, delete_link, media
):
    admin_client.post(delete_link)
    assert not Path(media.file.path).exists()


def test_theme_image_files_are_deleted_together_with_theme(
    admin_client, delete_link, image
):
    admin_client.post(delete_link)
    assert not Path(image.thumbnail.path).exists()


def test_theme_is_deleted_with_children(admin_client, delete_link, theme):
    Theme.objects.create(name="Child Theme", parent=theme)
    admin_client.post(delete_link)
    assert Theme.objects.count() == 1


def test_theme_children_are_deleted_recursively(admin_client, delete_link, theme):
    child_theme = Theme.objects.create(name="Child Theme", parent=theme)
    Theme.objects.create(name="Descendant Theme", parent=child_theme)
    Theme.objects.create(name="Descendant Theme", parent=child_theme)

    admin_client.post(delete_link)
    assert Theme.objects.count() == 1


def test_children_theme_can_be_deleted(admin_client, delete_link, theme, other_theme):
    theme.move_to(other_theme)
    theme.save()

    admin_client.post(delete_link)
    with pytest.raises(Theme.DoesNotExist):
        theme.refresh_from_db()


def test_deleting_children_theme_doesnt_delete_parent_themes(
    admin_client, delete_link, theme, other_theme
):
    theme.move_to(other_theme)
    theme.save()

    admin_client.post(delete_link)
    other_theme.refresh_from_db()


def test_deleting_theme_invalidates_themes_cache(admin_client, delete_link):
    with assert_invalidates_cache(THEME_CACHE):
        admin_client.post(delete_link)


def test_deleting_default_theme_sets_error_message(admin_client, default_theme):
    delete_link = reverse("misago:admin:themes:delete", kwargs={"pk": default_theme.pk})
    response = admin_client.post(delete_link)
    assert_has_error_message(response)


def test_default_theme_is_not_deleted(admin_client, default_theme):
    delete_link = reverse("misago:admin:themes:delete", kwargs={"pk": default_theme.pk})
    admin_client.post(delete_link)
    default_theme.refresh_from_db()


def test_deleting_active_theme_sets_error_message(admin_client, theme):
    theme.is_active = True
    theme.save()

    delete_link = reverse("misago:admin:themes:delete", kwargs={"pk": theme.pk})
    response = admin_client.post(delete_link)
    assert_has_error_message(response)


def test_active_theme_is_not_deleted(admin_client, theme):
    theme.is_active = True
    theme.save()

    delete_link = reverse("misago:admin:themes:delete", kwargs={"pk": theme.pk})
    admin_client.post(delete_link)
    theme.refresh_from_db()


def test_deleting_theme_containing_active_child_theme_sets_error_message(
    admin_client, theme, other_theme
):
    other_theme.move_to(theme)
    other_theme.is_active = True
    other_theme.save()

    delete_link = reverse("misago:admin:themes:delete", kwargs={"pk": theme.pk})
    response = admin_client.post(delete_link)
    assert_has_error_message(response)


def test_theme_containing_active_child_theme_is_not_deleted(
    admin_client, theme, other_theme
):
    other_theme.move_to(theme)
    other_theme.is_active = True
    other_theme.save()

    delete_link = reverse("misago:admin:themes:delete", kwargs={"pk": theme.pk})
    admin_client.post(delete_link)
    theme.refresh_from_db()
