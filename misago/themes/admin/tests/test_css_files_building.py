import pytest

from ....cache.test import assert_invalidates_cache
from ... import THEME_CACHE
from ..css import change_css_source, get_theme_media_map, rebuild_css
from ..tasks import build_single_theme_css, build_theme_css


@pytest.fixture
def assert_snapshot_match(snapshot, theme):
    def _assert_snapshot_match(result):
        result = result.replace(theme.dirname, "themedir")
        snapshot.assert_match(result)

    return _assert_snapshot_match


@pytest.fixture
def media_map(theme, image):
    return get_theme_media_map(theme)


def test_tasks_builds_single_css_file(theme, image, css_needing_build):
    build_single_theme_css(css_needing_build.pk)
    css_needing_build.refresh_from_db()
    assert css_needing_build.build_file


def test_tasks_skips_single_css_file_that_doesnt_require_build(theme, css):
    build_single_theme_css(css.pk)
    css.refresh_from_db()
    assert not css.build_file


def test_tasks_handles_nonexisting_css_file(db):
    build_single_theme_css(1)


def test_tasks_builds_theme_css_files_that_require_it(theme, image, css_needing_build):
    build_theme_css(theme.pk)
    css_needing_build.refresh_from_db()
    assert css_needing_build.build_file


def test_tasks_skips_theme_css_files_that_dont_require_build(theme, css):
    build_theme_css(theme.pk)
    css.refresh_from_db()
    assert not css.build_file


def test_tasks_handles_nonexisting_theme(nonexisting_theme):
    build_theme_css(nonexisting_theme.pk)


def test_media_map_for_theme_without_any_media_files_returns_empty_dict(theme):
    assert get_theme_media_map(theme) == {}


def test_media_map_for_theme_with_media_files_returns_dict_with_data(
    theme, image, media
):
    assert get_theme_media_map(theme)


def test_css_file_is_build(media_map, css_needing_build):
    rebuild_css(media_map, css_needing_build)
    css_needing_build.refresh_from_db()
    assert css_needing_build.build_file


def test_build_css_file_is_hashed(media_map, css_needing_build):
    rebuild_css(media_map, css_needing_build)
    css_needing_build.refresh_from_db()
    assert css_needing_build.build_hash


def test_build_css_file_includes_hash_in_filename(media_map, css_needing_build):
    rebuild_css(media_map, css_needing_build)
    css_needing_build.refresh_from_db()
    assert css_needing_build.build_hash in str(css_needing_build.build_file)


def test_build_css_file_has_size_set(media_map, css_needing_build):
    rebuild_css(media_map, css_needing_build)
    css_needing_build.refresh_from_db()
    assert css_needing_build.size


def test_simple_url_to_file_is_replaced_with_valid_url(
    assert_snapshot_match, media_map, image
):
    css = ".page-header { background-image: url(%s); }" % image.name
    result = change_css_source(media_map, css)
    assert_snapshot_match(result)


def test_relative_url_to_file_is_replaced_with_valid_url(
    assert_snapshot_match, media_map, image
):
    css = ".page-header { background-image: url(./%s); }" % image.name
    result = change_css_source(media_map, css)
    assert_snapshot_match(result)


def test_url_to_file_from_create_react_app_is_replaced_with_valid_url(
    assert_snapshot_match, media_map, image
):
    hashed_name = str(image.file).split("/")[-1]
    css = ".page-header { background-image: url(/static/media/%s); }" % hashed_name
    result = change_css_source(media_map, css)
    assert_snapshot_match(result)


def test_quoted_url_to_file_is_replaced_with_valid_url(
    assert_snapshot_match, media_map, image
):
    css = '.page-header { background-image: url("%s"); }' % image.name
    result = change_css_source(media_map, css)
    assert_snapshot_match(result)


def test_single_quoted_url_to_file_is_replaced_with_valid_url(
    assert_snapshot_match, media_map, image
):
    css = ".page-header { background-image: url('%s'); }" % image.name
    result = change_css_source(media_map, css)
    assert_snapshot_match(result)


def test_absolute_https_url_to_file_is_not_replaced(media_map):
    css = ".page-header { background-image: url(https://cdn.example.com/bg.png); }"
    result = change_css_source(media_map, css)
    assert result == css


def test_absolute_http_url_to_file_is_not_replaced(media_map):
    css = ".page-header { background-image: url(http://cdn.example.com/bg.png); }"
    result = change_css_source(media_map, css)
    assert result == css


def test_absolute_protocol_relative_url_to_file_is_not_replaced(media_map):
    css = ".page-header { background-image: url(://cdn.example.com/bg.png); }"
    result = change_css_source(media_map, css)
    assert result == css


def test_css_file_with_multiple_different_urls_is_correctly_replaced(
    assert_snapshot_match, media_map, image
):
    css = (
        ".page-header { background-image: url(http://cdn.example.com/bg.png); }"
        '\n.container { background-image: url("%s"); }'
        '\n.alert { background-image: url("%s"); }'
    ) % (image.name, str(image.file).strip("/")[-1])

    result = change_css_source(media_map, css)
    assert_snapshot_match(result)


def test_building_single_theme_css_invalidates_theme_cache(
    theme, image, css_needing_build
):
    with assert_invalidates_cache(THEME_CACHE):
        build_single_theme_css(css_needing_build.pk)


def test_building_theme_css_invalidates_theme_cache(theme):
    with assert_invalidates_cache(THEME_CACHE):
        build_theme_css(theme.pk)
