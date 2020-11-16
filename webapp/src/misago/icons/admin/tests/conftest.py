from io import BytesIO

import pytest
from PIL import Image
from django.urls import reverse


@pytest.fixture
def admin_link():
    return reverse("misago:admin:settings:icons:index")


def get_image(width, height):
    image = Image.new("RGBA", (width, height))
    buffer = BytesIO()
    image.save(buffer, "PNG")
    buffer.seek(0)
    return buffer.read()


@pytest.fixture
def image():
    return get_image(185, 185)


@pytest.fixture
def image_alt():
    return get_image(85, 85)


@pytest.fixture
def image_non_square():
    return get_image(180, 200)


@pytest.fixture
def image_small():
    return get_image(20, 20)
