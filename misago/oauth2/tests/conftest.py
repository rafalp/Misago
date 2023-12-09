from unittest.mock import patch

import pytest


def noop_filter_user_data(request, user, user_data):
    return user_data


@pytest.fixture
def disable_user_data_filters():
    with patch("misago.oauth2.validation.filter_user_data", noop_filter_user_data):
        yield
