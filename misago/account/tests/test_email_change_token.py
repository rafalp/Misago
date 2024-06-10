import pytest
from django.test import override_settings

from ..emailchange import (
    EmailChangeTokenError,
    create_email_change_token,
    read_email_change_token,
)


def test_email_change_token_can_be_created_and_unpacked(user):
    new_email = "email@example.com"
    token = create_email_change_token(user, new_email)
    token_email = read_email_change_token(user, token)
    assert new_email == token_email


def test_email_change_token_is_invalidated_by_user_email_change(user):
    token = create_email_change_token(user, "email@example.com")

    user.set_email("new@example.com")
    user.save()

    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, token)

    assert exc_info.value.args[0] == "invalid signature for message"


def test_email_change_token_is_invalidated_by_user_password_change(user):
    token = create_email_change_token(user, "email@example.com")

    user.set_password("changed")
    user.save()

    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, token)

    assert exc_info.value.args[0] == "invalid signature for message"


def test_email_change_token_is_invalidated_by_secret_key_change(user):
    token = create_email_change_token(user, "email@example.com")

    with override_settings(SECRET_KEY="NEW"):
        with pytest.raises(EmailChangeTokenError) as exc_info:
            read_email_change_token(user, token)

    assert exc_info.value.args[0] == "invalid signature for message"


def test_read_email_change_token_raises_error_if_token_is_invalid(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "invalid")

    assert exc_info.value.args[0] == "missing signature or message"


def test_read_email_change_token_raises_error_if_token_misses_signature(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "-invalid")

    assert exc_info.value.args[0] == "missing signature or message"


def test_read_email_change_token_raises_error_if_token_misses_message(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "invalid-")

    assert exc_info.value.args[0] == "missing signature or message"


def test_read_email_change_token_raises_error_if_token_signature_is_invalid(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "invalid-message")

    assert exc_info.value.args[0] == "invalid signature for message"


@override_settings(MISAGO_EMAIL_CHANGE_TOKEN_EXPIRES=0)
def test_read_email_change_token_raises_error_if_token_is_expired(user):
    token = create_email_change_token(user, "email@example.com")

    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, token)

    assert exc_info.value.args[0] == "token expired"
