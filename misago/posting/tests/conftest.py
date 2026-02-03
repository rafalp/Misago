import pytest
from django.core.exceptions import ValidationError

from ...permissions.proxy import UserPermissionsProxy
from ..hooks import validate_posted_contents_hook


@pytest.fixture
def mock_notify_on_new_thread_reply(mocker):
    return mocker.patch("misago.posting.views.reply.notify_on_new_thread_reply")


@pytest.fixture
def mock_upgrade_post_content(mocker):
    return mocker.patch("misago.posting.state.state.upgrade_post_content")


@pytest.fixture
def user_request(rf, cache_versions, dynamic_settings, user):
    request = rf.post("/post/")

    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    return request


@pytest.fixture
def posted_contents_validator():
    validate_posted_contents_hook.append_action(validate_spam_contents)
    yield
    validate_posted_contents_hook.clear_actions()


def validate_spam_contents(formset, state):
    # Check if posting form included thread title
    if formset.title and "spam" in state.thread.title.lower():
        raise ValidationError("Your message contains spam!")

    if "spam" in state.post.original.lower():
        raise ValidationError("Your message contains spam!")

    raise ValidationError("Your message contains spam!")
