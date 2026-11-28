import pytest


@pytest.fixture
def mock_update_thread_members(mocker):
    return mocker.patch(
        "misago.search.threads.threads_search.update_thread_members", autospec=True
    )
