import pytest
from django.forms import Form
from django.http import QueryDict

from ..fields import UserMultipleChoiceField
from ..models import User


@pytest.fixture
def users(admin, moderator, user, other_user):
    return (admin, moderator, user, other_user)


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


def test_user_multiple_choice_field_renders_with_form_initial_data(users, snapshot):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(initial={"users": users})

    field_html = str(form["users"])
    assert "users" in field_html

    for user in users:
        assert user.username in field_html
        assert f'value="{user.username}"' in field_html

    usernames = " ".join(user.username for user in users)
    assert f'value="{usernames}"' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_field_initial_data(users, snapshot):
    field_initial = users

    class TestForm(Form):
        users = UserMultipleChoiceField(initial=field_initial)

    form = TestForm()

    field_html = str(form["users"])
    assert "users" in field_html

    for user in users:
        assert user.username in field_html
        assert f'value="{user.username}"' in field_html

    usernames = " ".join(user.username for user in users)
    assert f'value="{usernames}"' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_data_for_chip_field(users, snapshot):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(
        QueryDict("&".join(f"users_chip={user.username}" for user in users))
    )

    field_html = str(form["users"])
    assert "users" in field_html

    for user in users:
        assert user.username in field_html
        assert f'value="{user.username}"' in field_html

    usernames = " ".join(user.username for user in users)
    assert f'value="{usernames}"' not in field_html
    assert 'value=""' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_data_for_text_field(users, snapshot):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    usernames = " ".join(user.username for user in users)

    form = TestForm(QueryDict(f"users_text={usernames}"))

    field_html = str(form["users"])
    assert "users" in field_html

    for user in users:
        assert user.username in field_html
        assert f'value="{user.username}"' not in field_html

    assert f'value="{usernames}"' in field_html
    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_cleaned_data_for_chip_field(
    users, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(
        QueryDict("&".join(f"users_chip={user.username}" for user in users))
    )
    assert form.is_valid()

    field_html = str(form["users"])
    assert "users" in field_html

    for user in users:
        assert user.username in field_html
        assert f'value="{user.username}"' in field_html

    usernames = " ".join(user.username for user in users)
    assert f'value="{usernames}"' not in field_html
    assert 'value=""' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_renders_with_cleaned_data_for_text_field(
    users, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    usernames = " ".join(user.username for user in users)

    form = TestForm(QueryDict(f"users_text={usernames}"))
    assert form.is_valid()

    field_html = str(form["users"])
    assert "users" in field_html

    for user in users:
        assert user.username in field_html
        assert f'value="{user.username}"' not in field_html

    assert f'value="{usernames}"' in field_html

    assert fuzz_html_user_ids(field_html, users) == snapshot


def test_user_multiple_choice_field_prioritizes_text_field(admin, other_user):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(
        QueryDict(f"users_chip={other_user.username}&users_text={admin.username}")
    )
    assert form.is_valid()
    assert form.cleaned_data["users"] == [admin]


def test_user_multiple_choice_field_validates_required_field():
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(QueryDict())
    assert not form.is_valid()
    assert form.errors == {"users": ["This field is required."]}


def test_user_multiple_choice_field_validates_chip_value_max_choices(
    admin, moderator, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField(max_choices=2)

    form = TestForm(
        QueryDict(
            f"users_chip={admin.username}&users_chip={moderator.username}&users_chip={other_user.username}"
        )
    )
    assert not form.is_valid()
    assert form.errors == {"users": ["Enter no more than 2 users."]}


def test_user_multiple_choice_field_validates_text_value_max_choices(
    admin, moderator, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField(max_choices=2)

    form = TestForm(
        QueryDict(
            f"users_text={admin.username} {moderator.username} {other_user.username}"
        )
    )
    assert not form.is_valid()
    assert form.errors == {"users": ["Enter no more than 2 users."]}


def test_user_multiple_choice_field_fails_to_validate_chip_value_nonexisting_users(
    admin, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField(max_choices=10)

    form = TestForm(
        QueryDict(f"users_chip=John&users_chip={admin.username}&users_chip=Doe")
    )
    assert not form.is_valid()
    assert form.errors == {"users": ["One or more users not found: John, Doe"]}

    field_html = str(form["users"])
    assert "users" in field_html
    assert fuzz_html_user_ids(field_html, [admin]) == snapshot


def test_user_multiple_choice_field_fails_to_validate_text_value_nonexisting_users(
    admin, snapshot
):
    class TestForm(Form):
        users = UserMultipleChoiceField(max_choices=10)

    form = TestForm(QueryDict(f"users_text=John {admin.username} Doe"))
    assert not form.is_valid()
    assert form.errors == {"users": ["One or more users not found: John, Doe"]}

    field_html = str(form["users"])
    assert "users" in field_html
    assert fuzz_html_user_ids(field_html, [admin]) == snapshot
