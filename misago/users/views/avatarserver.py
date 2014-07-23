from django.conf import settings
from django.contrib.auth import get_user_model

from misago.core.fileserver import make_file_response

from misago.users.avatars import set_default_avatar


def serve_avatar(request, user_id, size):
    avatar_file = get_avatar_file(user_id, size)
    avatar_path = '%s/%s.png' % (settings.MISAGO_AVATAR_CACHE, avatar_file)

    return make_file_response(avatar_path, 'image/png')


def get_avatar_file(user_id, size):
    if not size in settings.MISAGO_AVATARS_SIZES:
        for valid_size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
            if valid_size > size:
                size = valid_size

    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        file_formats = (user.joined_on.strftime('%y%m'), user.pk, size)
        return '%s/%s_%s' % file_formats
    except User.DoesNotExist:
        return 'guest_%s' % size

