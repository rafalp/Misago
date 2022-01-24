import pytest

from ...avatars.upload import store_uploaded_avatar
from ...uploads.store import media_file_exists
from ..delete import delete_user
from ..models import User


@pytest.mark.asyncio
async def test_user_is_deleted(user):
    await user.delete()

    with pytest.raises(User.DoesNotExist):
        await User.query.one(id=user.id)


@pytest.mark.asyncio
async def test_user_avatar_is_deleted_with_user(
    user, tmp_media_dir, create_upload_file
):
    avatar = await create_upload_file("avatar.png")
    user = await store_uploaded_avatar(user, avatar)
    assert user.avatars

    await user.delete()

    with pytest.raises(User.DoesNotExist):
        await User.query.one(id=user.id)

    for avatar in user.avatars:
        assert not media_file_exists(avatar["image"])


@pytest.mark.asyncio
async def test_delete_user_util_deletes_user_together_with_avatar(
    user, tmp_media_dir, create_upload_file
):
    avatar = await create_upload_file("avatar.png")
    user = await store_uploaded_avatar(user, avatar)
    assert user.avatars

    await delete_user(user)

    with pytest.raises(User.DoesNotExist):
        await User.query.one(id=user.id)

    for avatar in user.avatars:
        assert not media_file_exists(avatar["image"])
