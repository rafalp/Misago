import pytest
from django.test import override_settings

from ..emailchange import (
    EmailChangeTokenError,
    EmailChangeTokenErrorCode,
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

    assert str(exc_info.value) == "Mail change confirmation link has invalid signature."
    assert exc_info.value.code == EmailChangeTokenErrorCode.SIGNATURE_INVALID


def test_read_email_change_token_raises_error_if_token_is_invalid(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "invalid")

    assert str(exc_info.value) == "Mail change confirmation link is invalid."
    assert exc_info.value.code == EmailChangeTokenErrorCode.TOKEN_INVALID


def test_email_change_token_is_invalidated_by_user_password_change(user):
    token = create_email_change_token(user, "email@example.com")

    user.set_password("changed")
    user.save()

    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, token)

    assert str(exc_info.value) == "Mail change confirmation link has invalid signature."
    assert exc_info.value.code == EmailChangeTokenErrorCode.SIGNATURE_INVALID


def test_email_change_token_is_invalidated_by_secret_key_change(user):
    token = create_email_change_token(user, "email@example.com")

    with override_settings(SECRET_KEY="NEW"):
        with pytest.raises(EmailChangeTokenError) as exc_info:
            read_email_change_token(user, token)

    assert str(exc_info.value) == "Mail change confirmation link has invalid signature."
    assert exc_info.value.code == EmailChangeTokenErrorCode.SIGNATURE_INVALID


def test_read_email_change_token_raises_error_if_token_is_missing_signature(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "-invalid")

    assert (
        str(exc_info.value) == "Mail change confirmation link is missing a signature."
    )
    assert exc_info.value.code == EmailChangeTokenErrorCode.SIGNATURE_MISSING


def test_read_email_change_token_raises_error_if_token_is_missing_payload(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "invalid-")

    assert str(exc_info.value) == "Mail change confirmation link is missing a payload."
    assert exc_info.value.code == EmailChangeTokenErrorCode.PAYLOAD_MISSING


def test_read_email_change_token_raises_error_if_token_signature_is_invalid(user):
    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, "invalid-payload")

    assert str(exc_info.value) == "Mail change confirmation link has invalid signature."
    assert exc_info.value.code == EmailChangeTokenErrorCode.SIGNATURE_INVALID


@override_settings(MISAGO_EMAIL_CHANGE_TOKEN_EXPIRES=0)
def test_read_email_change_token_raises_error_if_token_is_expired(user):
    token = create_email_change_token(user, "email@example.com")

    with pytest.raises(EmailChangeTokenError) as exc_info:
        read_email_change_token(user, token)

    assert str(exc_info.value) == "Mail change confirmation link has expired."
    assert exc_info.value.code == EmailChangeTokenErrorCode.TOKEN_EXPIRED
