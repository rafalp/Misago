import pytest
from django.core.exceptions import ValidationError

from ...categories.models import Category
from ...permissions.enums import CategoryPermission
from ...posting.hooks import validate_posted_contents_hook
from ...testutils import grant_category_group_permissions


@pytest.fixture
def notify_on_new_private_thread_mock(mocker):
    return mocker.patch("misago.threads.participants.notify_on_new_private_thread")


@pytest.fixture
def notify_on_new_thread_reply_mock(mocker):
    return mocker.patch(
        "misago.threads.api.postingendpoint.notifications.notify_on_new_thread_reply"
    )


@pytest.fixture
def child_category(default_category, guests_group, members_group, moderators_group):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    for group in (guests_group, members_group, moderators_group):
        grant_category_group_permissions(
            child_category,
            group,
            CategoryPermission.SEE,
            CategoryPermission.BROWSE,
        )

    return child_category


@pytest.fixture
def hidden_category(root_category):
    hidden_category = Category(name="Hidden Category", slug="hidden-category")
    hidden_category.insert_at(root_category, position="last-child", save=True)
    return hidden_category


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
