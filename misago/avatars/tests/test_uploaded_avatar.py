import os

from PIL import Image
import pytest

from ...conf import settings
from ...uploads.store import make_media_path
from ..upload import store_uploaded_avatar


@pytest.mark.asyncio
async def test_uploaded_avatar_is_stored_on_user(user, uploaded_image, tmp_media_dir):
    updated_user = await store_uploaded_avatar(user, uploaded_image)
    assert len(updated_user.avatars) == len(settings.avatar_sizes)

    avatars_sizes = []
    for avatar in updated_user.avatars:
        assert avatar["size"] in settings.avatar_sizes
        assert avatar["size"] not in avatars_sizes
        avatars_sizes.append(avatar["size"])

    assert avatars_sizes == settings.avatar_sizes


@pytest.mark.asyncio
async def test_uploaded_avatar_is_stored_in_media(user, uploaded_image, tmp_media_dir):
    updated_user = await store_uploaded_avatar(user, uploaded_image)
    assert updated_user.avatars

    for avatar in updated_user.avatars:
        avatar_path = make_media_path(avatar["image"])
        assert os.path.isfile(avatar_path)


@pytest.mark.asyncio
async def test_uploaded_avatar_is_resized(user, uploaded_image, tmp_media_dir):
    updated_user = await store_uploaded_avatar(user, uploaded_image)
    assert updated_user.avatars

    for avatar in updated_user.avatars:
        avatar_path = make_media_path(avatar["image"])
        avatar_image = Image.open(avatar_path)
        assert avatar_image.size == (avatar["size"], avatar["size"])


@pytest.mark.asyncio
async def test_uploaded_avatar_replaces_previous_avatar(
    user, uploaded_image, tmp_media_dir
):
    user = await store_uploaded_avatar(user, uploaded_image)
    assert user.avatars

    updated_user = await store_uploaded_avatar(user, uploaded_image)
    assert updated_user.avatars

    updated_user.avatars != user.avatars

    for avatar in user.avatars:
        avatar_path = make_media_path(avatar["image"])
        assert not os.path.isfile(avatar_path)

    for avatar in updated_user.avatars:
        avatar_path = make_media_path(avatar["image"])
        assert os.path.isfile(avatar_path)
