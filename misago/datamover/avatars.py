from __future__ import unicode_literals

import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from misago.conf import settings
from misago.users.avatars import dynamic, gravatar, store, uploaded

from . import OLD_FORUM, fetch_assoc, movedids


UserModel = get_user_model()


def move_avatars(stdout, style):
    for old_user in fetch_assoc('SELECT * FROM misago_user ORDER BY id'):
        user = UserModel.objects.get(pk=movedids.get('user', old_user['id']))

        if old_user['avatar_ban'] or old_user['avatar_type'] == 'gallery':
            dynamic.set_avatar(user)
        else:
            if old_user['avatar_type'] == 'gravatar':
                try:
                    gravatar.set_avatar(user)
                except gravatar.GravatarError:
                    dynamic.set_avatar(user)
                    print_warning('%s: failed to download Gravatar' % user, stdout, style)
            else:
                try:
                    if not old_user['avatar_original'] or not old_user['avatar_crop']:
                        raise ValidationError("Invalid avatar upload data.")

                    image_path = os.path.join(
                        OLD_FORUM['MEDIA'], 'avatars', old_user['avatar_original']
                    )
                    image = uploaded.validate_dimensions(image_path)

                    cleaned_crop = convert_crop(image, old_user)
                    uploaded.clean_crop(image, cleaned_crop)

                    store.store_temporary_avatar(user, image)
                    uploaded.crop_source_image(user, 'tmp', cleaned_crop)
                except ValidationError as e:
                    dynamic.set_avatar(user)
                    print_warning('%s: %s' % (user, e.args[0]), stdout, style)

        user.save()


def print_warning(warning, stdout, style):
    stdout.write(style.ERROR(warning))


def convert_crop(image, user):
    min_size = max(settings.MISAGO_AVATARS_SIZES)
    x, y, s = [float(v) for v in user['avatar_crop'].split(',')]

    zoom = min_size / s

    return {
        'offset': {
            'x': x * zoom * -1,
            'y': y * zoom * -1,
        },
        'zoom': zoom,
    }
