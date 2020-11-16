import pytest

from .models import Icon


@pytest.fixture
def favicon(db):
    return Icon.objects.create(
        type=Icon.TYPE_FAVICON, image="static/favicon.png", size=1, width=48, height=48
    )


@pytest.fixture
def favicon_32(db):
    return Icon.objects.create(
        type=Icon.TYPE_FAVICON_32,
        image="static/favicon-32.png",
        size=1,
        width=32,
        height=32,
    )


@pytest.fixture
def favicon_16(db):
    return Icon.objects.create(
        type=Icon.TYPE_FAVICON_16,
        image="static/favicon-16.png",
        size=1,
        width=16,
        height=16,
    )


@pytest.fixture
def apple_touch_icon(db):
    return Icon.objects.create(
        type=Icon.TYPE_APPLE_TOUCH_ICON,
        image="static/test.png",
        size=1,
        width=180,
        height=180,
    )
