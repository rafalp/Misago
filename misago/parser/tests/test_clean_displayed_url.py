from ..urls import clean_displayed_url


def test_clean_displayed_url_strips_protocol():
    result = clean_displayed_url("https://misago-project.org")
    assert result == "misago-project.org"


def test_clean_displayed_url_strips_trailing_slash():
    result = clean_displayed_url("https://misago-project.org/")
    assert result == "misago-project.org"


def test_clean_displayed_url_keeps_trailing_slash_its_part_of_path():
    result = clean_displayed_url("https://misago-project.org/lorem/")
    assert result == "misago-project.org/lorem/"


def test_clean_displayed_url_shortens_long_path():
    result = clean_displayed_url(
        "https://en.wikipedia.org"
        "/wiki/Principles_of_user_interface_design_in_common_consumer_electronics"
    )
    assert result == "en.wikipedia.org/wiki/Principles_of_...consumer_electronics"


def test_clean_displayed_url_keeps_short_query_string():
    result = clean_displayed_url("https://misago-project.org/?sid=dsa7sdsa")
    assert result == "misago-project.org/?sid=dsa7sdsa"


def test_clean_displayed_url_shortens_long_query_string():
    result = clean_displayed_url(
        "https://misago-project.org/?sid=dsa7sdsa8s7a678ds6a786d8sa678d6as8778s6876d8a"
    )
    assert result == "misago-project.org/?sid=dsa7sdsa8s..."


def test_clean_displayed_url_strips_index_html():
    result = clean_displayed_url("https://misago-project.org/index.html")
    assert result == "misago-project.org"


def test_clean_displayed_url_strips_index_htm():
    result = clean_displayed_url("https://misago-project.org/index.htm")
    assert result == "misago-project.org"


def test_clean_displayed_url_strips_index_php():
    result = clean_displayed_url("https://misago-project.org/index.php")
    assert result == "misago-project.org"


def test_clean_displayed_url_strips_index_before_querystring():
    result = clean_displayed_url("https://misago-project.org/index.html?hello")
    assert result == "misago-project.org/?hello"


def test_clean_displayed_url_keeps_index_html_if_its_path_segment():
    result = clean_displayed_url("https://misago-project.org/index.php/")
    assert result == "misago-project.org/index.php/"
