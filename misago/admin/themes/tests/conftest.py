import os

import pytest
from django.urls import reverse

from ....themes.models import Theme


@pytest.fixture
def default_theme(db):
    return Theme.objects.get(is_default=True)


@pytest.fixture
def theme(db):
    return Theme.objects.create(name="Custom theme")


@pytest.fixture
def nonexisting_theme(mocker, default_theme):
    return mocker.Mock(pk=default_theme.pk + 1)


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def css(admin_client, theme):
    url = reverse("misago:admin:appearance:themes:upload-css", kwargs={"pk": theme.pk})
    with open(os.path.join(TESTS_DIR, "css", "test.css")) as fp:
        admin_client.post(url, {"assets": [fp]})
    return theme.css.last()


@pytest.fixture
def media(admin_client, theme):
    url = reverse(
        "misago:admin:appearance:themes:upload-media", kwargs={"pk": theme.pk}
    )
    with open(os.path.join(TESTS_DIR, "images", "test.svg")) as fp:
        admin_client.post(url, {"assets": [fp]})
    return theme.media.last()


@pytest.fixture
def image(admin_client, theme):
    url = reverse(
        "misago:admin:appearance:themes:upload-media", kwargs={"pk": theme.pk}
    )
    with open(os.path.join(TESTS_DIR, "images", "test.png"), "rb") as fp:
        admin_client.post(url, {"assets": [fp]})
    return theme.media.last()
