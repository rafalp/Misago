import os
from hashlib import md5
from io import BytesIO

from PIL import Image

from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.crypto import get_random_string

from misago.conf import settings


def normalize_image(image):
    """strip image of animation, convert to RGBA"""
    image.seek(0)
    return image.copy().convert('RGBA')


def store_avatar(user, image):
    from ..models import Avatar
    image = normalize_image(image)

    avatars = []
    for size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
        image_stream = BytesIO()

        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(image_stream, "PNG")

        avatars.append(Avatar.objects.create(
            user=user,
            size=size,
            image=ContentFile(image_stream.getvalue(), 'avatar')
        ))

    with transaction.atomic():
        user.avatars = [{'size': a.size, 'url': a.url} for a in avatars]
        user.save(update_fields=['avatars'])
        delete_avatar(user, exclude=[a.id for a in avatars])


def delete_avatar(user, exclude=None):
    exclude = exclude or []
    for avatar in user.avatar_set.exclude(id__in=exclude):
        avatar.image.delete(False)
    user.avatar_set.exclude(id__in=exclude).delete()


def upload_to(instance, filename):
    spread_path = md5(get_random_string(64).encode()).hexdigest()
    secret = get_random_string(32)
    filename_clean = '%s.png' % get_random_string(32)

    return os.path.join(
        'avatars', spread_path[:2], spread_path[2:4], secret, filename_clean)
