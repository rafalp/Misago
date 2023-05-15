import pytest


@pytest.fixture
def notify_on_new_private_thread_mock(mocker):
    return mocker.patch("misago.threads.participants.notify_on_new_private_thread")


@pytest.fixture
def notify_on_new_thread_reply_mock(mocker):
    return mocker.patch(
        "misago.threads.api.postingendpoint.notifications.notify_on_new_thread_reply"
    )
