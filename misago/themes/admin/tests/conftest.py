import os

import pytest
from django.urls import reverse

from ...models import Theme


@pytest.fixture
def default_theme(db):
    return Theme.objects.get(is_default=True)


@pytest.fixture
def theme(db):
    return Theme.objects.create(name="Custom theme")


@pytest.fixture
def other_theme(db):
    return Theme.objects.create(name="Other theme")


@pytest.fixture
def nonexisting_theme(mocker, default_theme):
    return mocker.Mock(pk=default_theme.pk + 1)


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def css(admin_client, theme, mock_build_theme_css):
    url = reverse("misago:admin:themes:upload-css", kwargs={"pk": theme.pk})
    with open(os.path.join(TESTS_DIR, "css", "test.css")) as fp:
        admin_client.post(url, {"assets": [fp]})
    return theme.css.get(name="test.css")


@pytest.fixture
def css_link(admin_client, theme):
    return theme.css.create(
        name="CSS link", url="https://example.com/cdn.css", order=theme.css.count()
    )


@pytest.fixture
def css_needing_build(admin_client, theme, mock_build_theme_css):
    url = reverse("misago:admin:themes:upload-css", kwargs={"pk": theme.pk})
    with open(os.path.join(TESTS_DIR, "css", "test.needs-build.css")) as fp:
        admin_client.post(url, {"assets": [fp]})
    return theme.css.get(name="test.needs-build.css")


@pytest.fixture
def media(admin_client, theme):
    url = reverse("misago:admin:themes:upload-media", kwargs={"pk": theme.pk})
    with open(os.path.join(TESTS_DIR, "images", "test.svg")) as fp:
        admin_client.post(url, {"assets": [fp]})
    return theme.media.get(name="test.svg")


@pytest.fixture
def image(admin_client, theme):
    url = reverse("misago:admin:themes:upload-media", kwargs={"pk": theme.pk})
    with open(os.path.join(TESTS_DIR, "images", "test.png"), "rb") as fp:
        admin_client.post(url, {"assets": [fp]})
    return theme.media.get(name="test.png")


@pytest.fixture(autouse=True)
def mock_build_single_theme_css(mocker):
    delay = mocker.Mock()
    mocker.patch(
        "misago.themes.admin.views.build_single_theme_css", mocker.Mock(delay=delay)
    )
    return delay


@pytest.fixture(autouse=True)
def mock_build_theme_css(mocker):
    delay = mocker.Mock()
    mocker.patch("misago.themes.admin.views.build_theme_css", mocker.Mock(delay=delay))
    mocker.patch(
        "misago.themes.admin.importer.build_theme_css", mocker.Mock(delay=delay)
    )
    return delay


@pytest.fixture(autouse=True)
def mock_update_remote_css_size(mocker):
    delay = mocker.Mock()
    mocker.patch(
        "misago.themes.admin.views.update_remote_css_size", mocker.Mock(delay=delay)
    )
    mocker.patch(
        "misago.themes.admin.importer.update_remote_css_size", mocker.Mock(delay=delay)
    )
    return delay
