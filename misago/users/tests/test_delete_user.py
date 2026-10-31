from pathlib import Path

import pytest

from ...privatethreads.models import PrivateThreadMember
from ...threads.models import Thread
from ..avatars import dynamic
from ..datadownloads import request_user_data_download
from ..delete import DeleteUserContentAction, delete_user
from ..models import Avatar, DataDownload


def test_delete_user_deletes_private_thread_if_it_has_no_other_members(
    user, user_private_thread
):
    PrivateThreadMember.objects.exclude(user=user).delete()

    delete_user(
        user, content_action=DeleteUserContentAction.LEAVE, anonymous_username="Anon"
    )

    with pytest.raises(Thread.DoesNotExist):
        user_private_thread.refresh_from_db()


def test_delete_user_leaves_private_thread_if_it_has_other_members(
    user, user_private_thread
):
    delete_user(
        user, content_action=DeleteUserContentAction.LEAVE, anonymous_username="Anon"
    )
    user_private_thread.refresh_from_db()


def test_delete_user_deletes_user_avatar_files(user):
    dynamic.set_avatar(user)
    user.save()

    user_avatars = []
    for avatar in user.avatar_set.all():
        avatar_path = Path(avatar.image.path)
        assert avatar_path.exists()
        assert avatar_path.is_file()
        user_avatars.append(avatar)
    assert user_avatars

    delete_user(
        user, content_action=DeleteUserContentAction.LEAVE, anonymous_username="Deleted"
    )

    for removed_avatar in user_avatars:
        avatar_path = Path(removed_avatar.image.path)
        assert not avatar_path.exists()
        assert not avatar_path.is_file()

        with pytest.raises(Avatar.DoesNotExist):
            Avatar.objects.get(pk=removed_avatar.pk)


def test_delete_user_also_deletes_their_data_downloads(user):
    data_download = request_user_data_download(user)
    delete_user(
        user, content_action=DeleteUserContentAction.LEAVE, anonymous_username="Deleted"
    )

    with pytest.raises(DataDownload.DoesNotExist):
        data_download.refresh_from_db()
