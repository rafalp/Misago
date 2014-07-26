from django.conf import settings
from django.contrib.auth import get_user_model

from misago.core.fileserver import make_file_response

from misago.users.avatars import set_default_avatar
from misago.users.avatars.uploaded import avatar_source_token


def serve_user_avatar(request, user_id, size):
    size = clean_size(size)
    User = get_user_model()

    if user_id > 0:
        try:
            user = User.objects.get(id=user_id)
            avatar_file = get_user_avatar_file(user, size)
        except User.DoesNotExist:
            avatar_file = get_blank_avatar_file(size)
    else:
        avatar_file = get_blank_avatar_file(size)

    avatar_path = '%s/%s.png' % (settings.MISAGO_AVATAR_STORE, avatar_file)
    return make_file_response(avatar_path, 'image/png')


def serve_user_avatar_source(request, user_id, token, type):
    fallback_avatar = get_blank_avatar_file(min(settings.MISAGO_AVATARS_SIZES))
    User = get_user_model()

    if user_id > 0:
        try:
            user = User.objects.get(id=user_id)
            if token == avatar_source_token(user, type):
                avatar_file = get_user_avatar_file(user, type)
            else:
                avatar_file = fallback_avatar
        except User.DoesNotExist:
            avatar_file = fallback_avatar
    else:
        avatar_file = fallback_avatar

    avatar_path = '%s/%s.png' % (settings.MISAGO_AVATAR_STORE, avatar_file)
    return make_file_response(avatar_path, 'image/png')


def serve_blank_avatar(request, size):
    size = clean_size(size)
    avatar_file = get_blank_avatar_file(size)
    avatar_path = '%s/%s.png' % (settings.MISAGO_AVATAR_STORE, avatar_file)
    return make_file_response(avatar_path, 'image/png')


def clean_size(size):
    if not size in settings.MISAGO_AVATARS_SIZES:
        size = max(settings.MISAGO_AVATARS_SIZES)
        for valid_size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
            if valid_size > size:
                size = valid_size
    return size


def get_user_avatar_file(user, size):
    file_formats = (user.joined_on.strftime('%y%m'), user.pk, size)
    return '%s/%s_%s' % file_formats


def get_blank_avatar_file(size):
    return 'blank/blank_%s' % size
