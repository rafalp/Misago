from ...users.models import Ban
from ..validators import UserDataValidator


def test_valid_data_passess_validation(db):
    validator = UserDataValidator(
        {"id": 1, "username": "User", "email": "user@example.com"}
    )
    assert validator.is_valid()
    assert "id" not in validator.errors
    assert "username" not in validator.errors
    assert "email" not in validator.errors


def test_invalid_id_fails_validation(db):
    validator = UserDataValidator(
        {"id": "invalid", "username": "User", "email": "user@example.com"}
    )
    assert not validator.is_valid()
    assert list(validator.errors) == ["id"]


def test_invalid_username_fails_validation(db):
    validator = UserDataValidator(
        {"id": 1, "username": "User!", "email": "user@example.com"}
    )
    assert not validator.is_valid()
    assert list(validator.errors) == ["username"]


def test_banned_username_fails_validation(db):
    Ban.objects.create(check_type=Ban.USERNAME, banned_value="User")
    validator = UserDataValidator(
        {"id": 1, "username": "User", "email": "user@example.com"}
    )
    assert not validator.is_valid()
    assert list(validator.errors) == ["username"]


def test_invalid_email_fails_validation(db):
    validator = UserDataValidator({"id": 1, "username": "User", "email": "invalid"})
    assert not validator.is_valid()
    assert list(validator.errors) == ["email"]


def test_banned_email_fails_validation(db):
    Ban.objects.create(check_type=Ban.EMAIL, banned_value="user@example.com")
    validator = UserDataValidator(
        {"id": 1, "username": "User", "email": "user@example.com"}
    )
    assert not validator.is_valid()
    assert list(validator.errors) == ["email"]


def test_is_active_flag_can_be_included_in_data(db):
    validator = UserDataValidator(
        {"id": 1, "username": "User", "email": "user@example.com", "is_active": True}
    )
    assert validator.is_valid()
    assert validator.cleaned_data["is_active"] is True
