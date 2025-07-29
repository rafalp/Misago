from django.forms import Form
from django.http import QueryDict

from ..fields import UserMultipleChoiceField


def test_user_multiple_choice_field_renders_without_data(snapshot):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm()

    field_html = str(form["users"])
    assert "users" in field_html
    assert field_html == snapshot


def test_user_multiple_choice_field_renders_with_form_initial_data(
    snapshot, admin, moderator, user, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(initial={"users": [admin, moderator, user, other_user]})

    field_html = str(form["users"])
    assert "users" in field_html
    assert admin.username in field_html
    assert f'value="{admin.slug}"' in field_html
    assert moderator.username in field_html
    assert f'value="{moderator.slug}"' in field_html
    assert user.username in field_html
    assert f'value="{user.slug}"' in field_html
    assert other_user.username in field_html
    assert f'value="{other_user.slug}"' in field_html

    usernames = " ".join(
        (admin.username, moderator.username, user.username, other_user.username)
    )
    assert f'value="{usernames}"' in field_html

    assert field_html == snapshot


def test_user_multiple_choice_field_renders_with_field_initial_data(
    snapshot, admin, moderator, user, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField(initial=[admin, moderator, user, other_user])

    form = TestForm()

    field_html = str(form["users"])
    assert "users" in field_html
    assert admin.username in field_html
    assert f'value="{admin.slug}"' in field_html
    assert moderator.username in field_html
    assert f'value="{moderator.slug}"' in field_html
    assert user.username in field_html
    assert f'value="{user.slug}"' in field_html
    assert other_user.username in field_html
    assert f'value="{other_user.slug}"' in field_html

    usernames = " ".join(
        (admin.username, moderator.username, user.username, other_user.username)
    )
    assert f'value="{usernames}"' in field_html

    assert field_html == snapshot


def test_user_multiple_choice_field_renders_without_query_data_for_field(
    snapshot, admin, moderator, user, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(
        QueryDict(
            "&".join(
                (
                    f"users={admin.username}",
                    f"users={moderator.username}",
                    f"users={user.username}",
                    f"users={other_user.username}",
                ),
            )
        )
    )

    field_html = str(form["users"])
    assert "users" in field_html

    # Bound but not yet cleaned data is useless for rendering purposes
    assert admin.username not in field_html
    assert f'value="{admin.slug}"' not in field_html
    assert moderator.username not in field_html
    assert f'value="{moderator.slug}"' not in field_html
    assert user.username not in field_html
    assert f'value="{user.slug}"' not in field_html
    assert other_user.username not in field_html
    assert f'value="{other_user.slug}"' not in field_html

    usernames = " ".join(
        (admin.username, moderator.username, user.username, other_user.username)
    )
    assert f'value="{usernames}"' not in field_html
    assert 'value=""' in field_html

    assert field_html == snapshot


def test_user_multiple_choice_field_renders_with_query_data_for_noscript_field(
    snapshot, admin, moderator, user, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    usernames = " ".join(
        (admin.username, moderator.username, user.username, other_user.username)
    )

    form = TestForm(QueryDict(f"users_noscript={usernames}"))

    field_html = str(form["users"])
    assert "users" in field_html
    assert admin.username in field_html
    assert f'value="{admin.slug}"' not in field_html
    assert moderator.username in field_html
    assert f'value="{moderator.slug}"' not in field_html
    assert user.username in field_html
    assert f'value="{user.slug}"' not in field_html
    assert other_user.username in field_html
    assert f'value="{other_user.slug}"' not in field_html
    assert f'value="{usernames}"' in field_html
    assert field_html == snapshot


def test_user_multiple_choice_field_renders_with_cleaned_query_data_for_field(
    snapshot, admin, moderator, user, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    form = TestForm(
        QueryDict(
            "&".join(
                (
                    f"users={admin.username}",
                    f"users={moderator.username}",
                    f"users={user.username}",
                    f"users={other_user.username}",
                ),
            )
        )
    )
    assert form.is_valid()

    field_html = str(form["users"])
    assert "users" in field_html
    assert admin.username in field_html
    assert f'value="{admin.slug}"' in field_html
    assert moderator.username in field_html
    assert f'value="{moderator.slug}"' in field_html
    assert user.username in field_html
    assert f'value="{user.slug}"' in field_html
    assert other_user.username in field_html
    assert f'value="{other_user.slug}"' in field_html

    usernames = " ".join(
        (admin.username, moderator.username, user.username, other_user.username)
    )
    assert f'value="{usernames}"' not in field_html
    assert 'value=""' in field_html

    assert field_html == snapshot


def test_user_multiple_choice_field_renders_with_cleaned_query_data_for_noscript_field(
    snapshot, admin, moderator, user, other_user
):
    class TestForm(Form):
        users = UserMultipleChoiceField()

    usernames = " ".join(
        (admin.username, moderator.username, user.username, other_user.username)
    )

    form = TestForm(QueryDict(f"users_noscript={usernames}"))
    assert form.is_valid()

    field_html = str(form["users"])
    assert "users" in field_html
    assert admin.username in field_html
    assert f'value="{admin.slug}"' not in field_html
    assert moderator.username in field_html
    assert f'value="{moderator.slug}"' not in field_html
    assert user.username in field_html
    assert f'value="{user.slug}"' not in field_html
    assert other_user.username in field_html
    assert f'value="{other_user.slug}"' not in field_html
    assert f'value="{usernames}"' in field_html
    assert field_html == snapshot
