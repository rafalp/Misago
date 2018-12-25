import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


def test_get_user_by_username(db):
    user = User.objects.create_user("User", "test@example.com")
    assert User.objects.get_by_username("User") == user


def test_getting_user_by_username_is_case_insensitive(db):
    user = User.objects.create_user("User", "test@example.com")
    assert User.objects.get_by_username("uSeR") == user


def test_getting_user_by_username_raises_does_not_exist_for_no_result(db):
    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_username("user")


def test_getting_user_by_username_supports_diacritics(db):
    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_username("łóć")


def test_getting_user_by_username_is_not_doing_fuzzy_matching(db):
    User.objects.create_user("User", "test@example.com")
    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_username("usar")


def test_get_user_by_email(db):
    user = User.objects.create_user("User", "test@example.com")
    assert User.objects.get_by_email("test@example.com") == user


def test_getting_user_by_email_is_case_insensitive(db):
    user = User.objects.create_user("User", "test@example.com")
    assert User.objects.get_by_email("tEsT@eXaMplE.com") == user


def test_getting_user_by_email_supports_diacritics(db):
    user = User.objects.create_user("User", "łóć@łexĄmple.com")
    assert User.objects.get_by_email("łÓć@ŁexĄMple.com") == user


def test_getting_user_by_email_raises_does_not_exist_for_no_result(db):
    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_email("test@example.com")


def test_get_user_by_username_using_combined_getter(db):
    user = User.objects.create_user("User", "test@example.com")
    assert User.objects.get_by_username_or_email("user") == user


def test_get_user_by_email_using_combined_getter(db):
    user = User.objects.create_user("User", "test@example.com")
    assert User.objects.get_by_username_or_email("test@example.com") == user


def test_combined_getter_handles_username_slug_and_email_collision(db):
    email_match = User.objects.create_user("Bob", "test@test.test")
    slug_match = User.objects.create_user("TestTestTest", "other@test.com")

    assert User.objects.get_by_username_or_email("test@test.test") == email_match
    assert User.objects.get_by_username_or_email("TestTestTest") == slug_match


def test_combined_getter_raises_does_not_exist_for_no_result(db):
    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_username_or_email("User")
