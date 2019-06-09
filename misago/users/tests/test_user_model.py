from pathlib import Path

import pytest

from ...conf import settings
from ...core.utils import slugify
from ..avatars import dynamic
from ..datadownloads import request_user_data_download
from ..models import Avatar, DataDownload, User
from ..utils import hash_email


def test_username_and_slug_is_anonymized(user):
    user.anonymize_data(anonymous_username="Deleted")
    assert user.username == "Deleted"
    assert user.slug == slugify("Deleted")


def test_user_avatar_files_are_deleted_during_user_deletion(user):
    dynamic.set_avatar(user)
    user.save()

    user_avatars = []
    for avatar in user.avatar_set.all():
        avatar_path = Path(avatar.image.path)
        assert avatar_path.exists()
        assert avatar_path.is_file()
        user_avatars.append(avatar)
    assert user_avatars

    user.delete(anonymous_username="Deleted")

    for removed_avatar in user_avatars:
        avatar_path = Path(removed_avatar.image.path)
        assert not avatar_path.exists()
        assert not avatar_path.is_file()

        with pytest.raises(Avatar.DoesNotExist):
            Avatar.objects.get(pk=removed_avatar.pk)


def test_username_setter_also_sets_slug():
    user = User()
    user.set_username("TestUser")
    assert user.username == "TestUser"
    assert user.slug == "testuser"


def test_django_username_getters_return_username(user):
    assert user.get_username() == user.username
    assert user.get_full_name() == user.username
    assert user.get_short_name() == user.username


def test_email_setter_normalizes_email():
    user = User()
    user.set_email("us3R@EXample.com")
    assert user.email == "us3R@example.com"


def test_email_setter_also_sets_email_hash():
    user = User()
    user.set_email("us3R@example.com")
    assert user.email_hash == hash_email("us3R@example.com")


def test_real_name_getter_returns_name_entered_in_profile_field(user):
    user.profile_fields["real_name"] = "John Doe"
    assert user.get_real_name() == "John Doe"


def test_real_name_getter_returns_none_if_profile_field_has_no_value(user):
    assert user.get_real_name() is None


def test_marking_user_for_deletion_deactivates_their_account_in_db(user):
    user.mark_for_delete()
    assert not user.is_active
    assert user.is_deleting_account

    user.refresh_from_db()
    assert not user.is_active
    assert user.is_deleting_account


def test_user_data_downloads_are_removed_by_anonymization(user):
    data_download = request_user_data_download(user)
    user.anonymize_data(anonymous_username="Deleted")

    with pytest.raises(DataDownload.DoesNotExist):
        data_download.refresh_from_db()


def test_deleting_user_also_deletes_their_data_downloads(user):
    data_download = request_user_data_download(user)
    user.delete(anonymous_username="Deleted")

    with pytest.raises(DataDownload.DoesNotExist):
        data_download.refresh_from_db()
