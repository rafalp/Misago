from unittest.mock import Mock

import pytest

from ..poststracker import save_read


@pytest.fixture
def read_thread(user, thread):
    save_read(user, thread.first_post)
    return thread


@pytest.fixture
def anonymous_request_mock(dynamic_settings, anonymous_user, anonymous_user_acl):
    return Mock(
        settings=dynamic_settings, user=anonymous_user, user_acl=anonymous_user_acl
    )


@pytest.fixture
def request_mock(dynamic_settings, user, user_acl):
    return Mock(settings=dynamic_settings, user=user, user_acl=user_acl)
