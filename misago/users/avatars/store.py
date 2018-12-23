import os
from hashlib import md5
from io import BytesIO

from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from PIL import Image

from ...conf import settings


def normalize_image(image):
    """strip image of animation, convert to RGBA"""
    image.seek(0)
    return image.copy().convert("RGBA")


def delete_avatar(user, delete_tmp=True, delete_src=True):
    if delete_tmp and user.avatar_tmp:
        user.avatar_tmp.delete(save=False)

    if delete_src and user.avatar_src:
        user.avatar_src.delete(save=False)

    for avatar in user.avatar_set.all():
        avatar.image.delete(save=False)
    user.avatar_set.all().delete()


def store_avatar(user, image):
    from ..models import Avatar

    image = normalize_image(image)

    avatars = []
    for size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
        image_stream = BytesIO()

        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(image_stream, "PNG")

        avatars.append(
            Avatar.objects.create(
                user=user,
                size=size,
                image=ContentFile(image_stream.getvalue(), "avatar"),
            )
        )

    user.avatars = [{"size": a.size, "url": a.url} for a in avatars]
    user.save(update_fields=["avatars"])


def store_new_avatar(user, image, delete_tmp=True, delete_src=True):
    delete_avatar(user, delete_tmp=delete_tmp, delete_src=delete_src)
    store_avatar(user, image)


def store_temporary_avatar(user, image):
    image_stream = BytesIO()

    normalize_image(image)
    image.save(image_stream, "PNG")

    if user.avatar_tmp:
        user.avatar_tmp.delete(save=False)

    user.avatar_tmp = ContentFile(image_stream.getvalue(), "avatar")
    user.save(update_fields=["avatar_tmp"])


def store_original_avatar(user):
    if user.avatar_src:
        user.avatar_src.delete(save=False)
    user.avatar_src = user.avatar_tmp
    user.avatar_tmp = None
    user.save(update_fields=["avatar_tmp", "avatar_src"])


def upload_to(instance, filename):
    spread_path = md5(get_random_string(64).encode()).hexdigest()
    secret = get_random_string(32)
    filename_clean = "%s.png" % get_random_string(32)

    return os.path.join(
        "avatars", spread_path[:2], spread_path[2:4], secret, filename_clean
    )
