import pytest
import pytest_asyncio
from PIL import Image

from ...conf import settings
from ...uploads.store import make_media_path, media_file_exists
from ..upload import store_uploaded_avatar


@pytest_asyncio.fixture
async def uploaded_image(create_upload_file):
    return await create_upload_file("avatar.png")


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
        assert media_file_exists(avatar["image"])


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

    assert updated_user.avatars != user.avatars

    for avatar in user.avatars:
        assert not media_file_exists(avatar["image"])

    for avatar in updated_user.avatars:
        assert media_file_exists(avatar["image"])
