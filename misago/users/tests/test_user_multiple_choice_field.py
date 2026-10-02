import pytest
from django.forms import Form
from django.http import QueryDict

from ..fields import UserMultipleChoiceField
from ..models import User


@pytest.fixture
def users(admin, moderator, user, other_user):
    return (admin, moderator, user, other_user)


@pytest.fixture
def usernames(users):
    return ", ".join(user.username for user in users)


def fuzz_html_user_ids(html_str: str, users: list[User]) -> str:
    for new_id, user in enumerate(users, 1000):
        html_str = html_str.replace(f'id="{user.id}"', f'id="{new_id}"')
    return html_str


def test_user_multiple_choice_field_renders_without_data(snapshot):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm()

    field_html = str(form["users"])
    assert "users" in field_html
    assert field_html == snapshot


def test_user_multiple_choice_field_renders_with_form_initial_data(
    users, usernames, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(initial={"users": users})

    field_html = str(form["users"])
    assert "users" in field_html
    assert f'value="{usernames}"' in field_html

    for user in users:
        assert user.username in field_html
        assert f'-id="{user.id}"' in field_html
        assert f'-name="{user.username}"' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_field_initial_data(
    users, usernames, snapshot
):
    field_initial = users

    class TestForm(Form):
        users = UserMultipleChoiceField(initial=field_initial)

    form = TestForm()

    field_html = str(form["users"])
    assert "users" in field_html
    assert f'value="{usernames}"' in field_html

    for user in users:
        assert user.username in field_html
        assert f'-id="{user.id}"' in field_html
        assert f'-name="{user.username}"' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_submitted_data(
    users, usernames, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(QueryDict(f"users={usernames}"))

    field_html = str(form["users"])
    assert "users" in field_html
    assert f'value="{usernames}"' in field_html

    for user in users:
        assert user.username in field_html
        assert f'-id="{user.id}"' in field_html
        assert f'-name="{user.username}"' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_cleaned_data(
    users, usernames, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(QueryDict(f"users={usernames}"))
    assert form.is_valid()

    field_html = str(form["users"])
    assert "users" in field_html
    assert f'value="{usernames}"' in field_html

    for user in users:
        assert user.username in field_html
        assert f'-id="{user.id}"' in field_html
        assert f'-name="{user.username}"' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_validates_required_field():
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(QueryDict())
    assert not form.is_valid()
    assert form.errors == {"users": ["This field is required."]}


def test_user_multiple_choice_field_validates_max_choices(usernames):
    class TestForm(Form):
        users = UserMultipleChoiceField(max_choices=2)

    form = TestForm(QueryDict(f"users={usernames}"))
    assert not form.is_valid()
    assert form.errors == {"users": ["Enter no more than 2 users."]}


def test_user_multiple_choice_field_fails_to_validate_nonexisting_users(
    admin, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField(max_choices=10)

    form = TestForm(QueryDict(f"users=John, {admin.username}, Doe"))
    assert not form.is_valid()
    assert form.errors == {"users": ["One or more users not found: John, Doe"]}

    field_html = str(form["users"])
    assert "users" in field_html
    assert fuzz_html_user_ids(field_html, [admin]) == snapshot
