from hashlib import md5
from typing import TYPE_CHECKING, Dict


from PIL import Image
from asgiref.sync import sync_to_async

from ..conf import settings
from ..uploads.store import (
    delete_media_file,
    make_media_directory,
    make_media_path,
    media_file_exists,
)
from ..utils.strings import get_random_string
from .types import AvatarType

if TYPE_CHECKING:
    from ..users.models import User


async def store_user_avatar(
    user: "User", avatar_type: AvatarType, image: Image
) -> "User":
    sizes_paths = await get_unique_sizes_paths(user.id)
    for size, path in sizes_paths.items():
        await store_user_avatar_image(image, size, path)

    await delete_user_avatars(user)

    avatars = [{"size": size, "image": path} for size, path in sizes_paths.items()]

    return await user.update(avatar_type=avatar_type, avatars=avatars)


@sync_to_async
def get_unique_sizes_paths(user_id: int, extension: str = "png") -> Dict[int, str]:
    paths = {}

    user_hash = md5(str(user_id).encode("utf-8")).hexdigest()
    prefix = "avatars/%s/%s" % (user_hash[0:2], user_hash[2:4])

    make_media_directory(prefix)

    for size in settings.avatar_sizes:
        while True:
            random_suffix = get_random_string(4)
            size_path = f"{prefix}/{size}_{random_suffix}.{extension}"
            if not media_file_exists(size_path):
                paths[size] = size_path
                break

    return paths


@sync_to_async
def store_user_avatar_image(image: Image, size: int, path: str):
    resized_image = image.resize((size, size))
    resized_image.save(make_media_path(path))


@sync_to_async
def delete_user_avatars(user: "User"):
    for avatar in user.avatars:
        delete_media_file(avatar["image"])
