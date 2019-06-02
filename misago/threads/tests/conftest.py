import pytest

from ..test import post_thread


@pytest.fixture
def post(default_category):
    return post_thread(default_category).first_post