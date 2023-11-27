from .. import discover
from ..manifest import MisagoPlugin
from ..metadata import (
    clean_plugin_color,
    clean_plugin_icon,
    clean_plugin_str,
    clean_plugin_url,
    create_plugin_metadata,
)


def test_plugin_metadata_is_created_without_manifest():
    metadata = create_plugin_metadata("plugin_package", discover, None, None)

    assert metadata.package == "plugin_package"
    assert metadata.dirname == "misago"
    assert metadata.has_manifest is False
    assert metadata.manifest_error is None
    assert metadata.name is None
    assert metadata.description is None
    assert metadata.license is None
    assert metadata.icon is None
    assert metadata.color is None
    assert metadata.version is None
    assert metadata.author is None
    assert metadata.homepage is None
    assert metadata.sponsor is None
    assert metadata.help is None
    assert metadata.bugs is None
    assert metadata.repo is None


def test_plugin_metadata_is_created_with_manifest_error():
    metadata = create_plugin_metadata(
        "plugin_package", discover, None, "Not found error."
    )

    assert metadata.package == "plugin_package"
    assert metadata.dirname == "misago"
    assert metadata.has_manifest is False
    assert metadata.manifest_error == "Not found error."
    assert metadata.name is None
    assert metadata.description is None
    assert metadata.license is None
    assert metadata.icon is None
    assert metadata.color is None
    assert metadata.version is None
    assert metadata.author is None
    assert metadata.homepage is None
    assert metadata.sponsor is None
    assert metadata.help is None
    assert metadata.bugs is None
    assert metadata.repo is None


def test_plugin_metadata_is_created_from_empty_manifest():
    manifest = MisagoPlugin()
    metadata = create_plugin_metadata(
        "plugin_package",
        discover,
        manifest,
        None,
    )

    assert metadata.package == "plugin_package"
    assert metadata.dirname == "misago"
    assert metadata.has_manifest is True
    assert metadata.manifest_error is None
    assert metadata.name is None
    assert metadata.description is None
    assert metadata.license is None
    assert metadata.icon is None
    assert metadata.color is None
    assert metadata.version is None
    assert metadata.author is None
    assert metadata.homepage is None
    assert metadata.sponsor is None
    assert metadata.help is None
    assert metadata.bugs is None
    assert metadata.repo is None


def test_plugin_metadata_is_created_from_valid_full_manifest():
    manifest = MisagoPlugin(
        name="Test plugin",
        description="Test plugin's manifest",
        license="GNU GPL v2",
        icon="fa fa-puzzle",
        color="#FF00F0",
        version="1.0",
        author="Lorem Ipsum",
        homepage="https://misago-project.org",
        sponsor="https://sponsor.misago-project.org",
        help="https://help.misago-project.org",
        bugs="https://bugs.misago-project.org",
        repo="https://repo.misago-project.org",
    )

    metadata = create_plugin_metadata(
        "plugin_package",
        discover,
        manifest,
        None,
    )

    assert metadata.package == "plugin_package"
    assert metadata.dirname == "misago"
    assert metadata.has_manifest is True
    assert metadata.manifest_error is None
    assert metadata.name == "Test plugin"
    assert metadata.description == "Test plugin's manifest"
    assert metadata.license == "GNU GPL v2"
    assert metadata.icon == "fa fa-puzzle"
    assert metadata.color == "#FF00F0"
    assert metadata.version == "1.0"
    assert metadata.author == "Lorem Ipsum"
    assert metadata.homepage.netloc == "misago-project.org"
    assert metadata.homepage.url == "https://misago-project.org"
    assert metadata.sponsor.netloc == "sponsor.misago-project.org"
    assert metadata.sponsor.url == "https://sponsor.misago-project.org"
    assert metadata.help.netloc == "help.misago-project.org"
    assert metadata.help.url == "https://help.misago-project.org"
    assert metadata.bugs.netloc == "bugs.misago-project.org"
    assert metadata.bugs.url == "https://bugs.misago-project.org"
    assert metadata.repo.netloc == "repo.misago-project.org"
    assert metadata.repo.url == "https://repo.misago-project.org"


def test_plugin_color_returns_none_if_manifest_value_is_none():
    assert clean_plugin_color(None) is None


def test_plugin_color_returns_none_if_manifest_value_is_not_a_str():
    assert clean_plugin_color([1, 2, 3]) is None
    assert clean_plugin_color({}) is None
    assert clean_plugin_color(False) is None
    assert clean_plugin_color(42) is None


def test_plugin_color_returns_none_if_manifest_value_is_invalid_str():
    assert clean_plugin_color("") is None
    assert clean_plugin_color("red") is None
    assert clean_plugin_color("#8823412") is None
    assert clean_plugin_color("#zzzzzz") is None
    assert clean_plugin_color("eke eke nii") is None


def test_plugin_color_returns_valid_manifest_color():
    assert clean_plugin_color("#ffffff") == "#FFFFFF"
    assert clean_plugin_color("#000000") == "#000000"


def test_plugin_icon_returns_none_if_manifest_value_is_none():
    assert clean_plugin_icon(None) is None


def test_plugin_icon_returns_none_if_manifest_value_is_not_a_str():
    assert clean_plugin_icon([1, 2, 3]) is None
    assert clean_plugin_icon({}) is None
    assert clean_plugin_icon(False) is None
    assert clean_plugin_icon(42) is None


def test_plugin_icon_returns_none_if_manifest_value_is_invalid_str():
    assert clean_plugin_icon("") is None
    assert clean_plugin_icon("red") is None
    assert clean_plugin_icon("bell clock") is None
    assert clean_plugin_icon("fas other") is None


def test_plugin_icon_returns_valid_manifest_icon():
    assert clean_plugin_icon("fa fa-test") == "fa fa-test"
    assert clean_plugin_icon("fas fa-other-test") == "fas fa-other-test"
    assert clean_plugin_icon("far fa-extra-test") == "far fa-extra-test"


def test_plugin_str_returns_none_if_manifest_value_is_none():
    assert clean_plugin_str(None, 10) is None


def test_plugin_str_returns_none_if_manifest_value_is_not_a_str():
    assert clean_plugin_str([1, 2, 3], 10) is None
    assert clean_plugin_str({}, 10) is None
    assert clean_plugin_str(False, 10) is None
    assert clean_plugin_str(42, 10) is None


def test_plugin_str_returns_none_if_manifest_value_is_empty_str():
    assert clean_plugin_str("", 10) is None
    assert clean_plugin_str("  ", 10) is None


def test_plugin_str_returns_string_cut_to_length():
    assert clean_plugin_str("Hello world", 15) == "Hello world"
    assert clean_plugin_str("Hello world", 5) == "Hello"


def test_plugin_str_returns_string_with_whitespace_stripped():
    assert clean_plugin_str("    Hello world   ", 15) == "Hello world"
    assert clean_plugin_str("  Hello world  ", 5) == "Hello"


def test_plugin_url_returns_none_if_manifest_value_is_none():
    assert clean_plugin_url(None) is None


def test_plugin_url_returns_none_if_manifest_value_is_not_a_str():
    assert clean_plugin_url([1, 2, 3]) is None
    assert clean_plugin_url({}) is None
    assert clean_plugin_url(False) is None
    assert clean_plugin_url(42) is None


def test_plugin_url_returns_none_if_manifest_value_is_invalid_str():
    assert clean_plugin_url("") is None
    assert clean_plugin_url("red") is None
    assert clean_plugin_url("misago-project.org") is None
    assert clean_plugin_url("www.misago-project.org") is None
    assert clean_plugin_url('javascript:alert("test")') is None
    assert clean_plugin_url("mailto:dot@exc.com") is None
    assert clean_plugin_url("ftp://oke.com/guru") is None


def test_plugin_url_returns_url_if_manifest_value_is_supported_url():
    http_url = clean_plugin_url("http://example.com")
    assert http_url.netloc == "example.com"
    assert http_url.url == "http://example.com"

    https_url = clean_plugin_url("https://example.com")
    assert https_url.netloc == "example.com"
    assert https_url.url == "https://example.com"

    comma_url = clean_plugin_url("https://example-site.com")
    assert comma_url.netloc == "example-site.com"
    assert comma_url.url == "https://example-site.com"

    digits_url = clean_plugin_url("https://example-site365.com")
    assert digits_url.netloc == "example-site365.com"
    assert digits_url.url == "https://example-site365.com"

    https_www_url = clean_plugin_url("https://www.example.com")
    assert https_www_url.netloc == "www.example.com"
    assert https_www_url.url == "https://www.example.com"

    https_www_subdomains_url = clean_plugin_url("https://www.dev.stage.example.com")
    assert https_www_subdomains_url.netloc == "www.dev.stage.example.com"
    assert https_www_subdomains_url.url == "https://www.dev.stage.example.com"

    http_php_url = clean_plugin_url("http://example.com/some/where.php")
    assert http_php_url.netloc == "example.com"
    assert http_php_url.url == "http://example.com/some/where.php"

    http_path_url = clean_plugin_url("http://example.com/some-path/ok/123")
    assert http_path_url.netloc == "example.com"
    assert http_path_url.url == "http://example.com/some-path/ok/123"

    http_fragment_url = clean_plugin_url("http://example.com/some-path/#ok-123")
    assert http_fragment_url.netloc == "example.com"
    assert http_fragment_url.url == "http://example.com/some-path/#ok-123"

    http_query_url = clean_plugin_url("http://example.com/arg/?ok=yes&alt=no")
    assert http_query_url.netloc == "example.com"
    assert http_query_url.url == "http://example.com/arg/?ok=yes&alt=no"
