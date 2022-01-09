from math import ceil
from typing import TYPE_CHECKING

from PIL import Image
from asgiref.sync import sync_to_async
from starlette.datastructures import UploadFile

from .store import store_user_avatar
from .types import AvatarType

if TYPE_CHECKING:
    from ..users.models import User


async def store_uploaded_avatar(user: "User", avatar: UploadFile) -> "User":
    cropped_image = await crop_avatar_file(avatar)
    return await store_user_avatar(user, AvatarType.UPLOAD, cropped_image)


@sync_to_async
def crop_avatar_file(value: UploadFile) -> Image:
    img = Image.open(value.file)

    width, height = img.size
    box = min(img.size)
    if width > height:
        left = ceil((width - box) / 2)
        img = img.crop((left, 0, left + box, box))
    else:
        top = ceil((height - box) / 2)
        img = img.crop((0, top, box, top + box))

    return img
