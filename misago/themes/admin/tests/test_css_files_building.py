import pytest

from ..css import change_css_source, get_theme_media_map


@pytest.fixture
def assert_snapshot_match(snapshot, theme):
    def _assert_snapshot_match(result):
        result = result.replace(theme.dirname, "themedir")
        snapshot.assert_match(result)

    return _assert_snapshot_match


@pytest.fixture
def media_map(theme, image):
    return get_theme_media_map(theme)


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
