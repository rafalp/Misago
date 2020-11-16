import pytest
from django.contrib.auth import get_user_model

from ..models import Rank
from ..utils import hash_email

User = get_user_model()


def test_user_is_created(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.pk
    assert user.joined_on


def test_user_is_created_with_username_and_slug(db):
    user = User.objects.create_user("UserName", "test@example.com")
    assert user.slug == "username"


def test_user_is_created_with_normalized_email_and_email_hash(db):
    user = User.objects.create_user("User", "test@eXamPLe.com")
    assert user.email == "test@example.com"
    assert user.email_hash == hash_email(user.email)


def test_user_is_created_with_online_tracker(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.online_tracker
    assert user.online_tracker.last_click == user.last_login


def test_user_is_created_with_useable_password(db):
    password = "password"
    user = User.objects.create_user("UserUserame", "test@example.com", password)
    assert user.check_password(password)


def test_user_is_created_with_default_rank(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.rank == Rank.objects.get_default()


def test_user_is_created_with_custom_rank(db):
    rank = Rank.objects.create(name="Test rank")
    user = User.objects.create_user("User", "test@example.com", rank=rank)
    assert user.rank == rank


def test_newly_created_user_last_login_is_same_as_join_date(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.last_login == user.joined_on


def test_user_is_created_with_authenticated_role(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.roles.get(special_role="authenticated")


def test_user_is_created_with_diacritics_in_email(db):
    email = "łóć@łexąmple.com"
    user = User.objects.create_user("UserName", email)
    assert user.email == email


def test_creating_user_without_username_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_user("", "test@example.com")


def test_creating_user_without_email_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_user("User", "")


def test_create_superuser(db):
    user = User.objects.create_superuser("User", "test@example.com")
    assert user.is_staff
    assert user.is_superuser


def test_superuser_is_created_with_team_rank(db):
    user = User.objects.create_superuser("User", "test@example.com")
    assert "team" in str(user.rank)


def test_creating_superuser_without_staff_status_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_superuser("User", "test@example.com", is_staff=False)


def test_creating_superuser_without_superuser_status_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_superuser("User", "test@example.com", is_superuser=False)
