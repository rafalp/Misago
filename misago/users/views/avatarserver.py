import os

from path import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control, never_cache

from misago.core.fileserver import make_file_response

from misago.users.avatars import store


@cache_control(private=True, must_revalidate=True, max_age=5 * 24 * 3600)
def serve_blank_avatar(request, size):
    size = clean_size(size)
    avatar_dir = store.get_avatars_dir_path()
    avatar_file = get_blank_avatar_file(size)
    avatar_path = os.path.join(avatar_dir, avatar_file)
    return make_file_response(avatar_path, 'image/png')


@cache_control(private=True, must_revalidate=False)
def serve_user_avatar(request, hash, user_id, size):
    size = clean_size(size)

    if int(user_id) > 0:
        avatar_dir = store.get_avatars_dir_path(user_id)
        avatar_file = get_user_avatar_file(user_id, size)
        avatar_path = os.path.join(avatar_dir, avatar_file)

        if Path(avatar_path).exists():
            avatar_path = os.path.join(avatar_dir, avatar_file)
            return make_file_response(avatar_path, 'image/png')
        else:
            return serve_blank_avatar(request, size)
    else:
        return serve_blank_avatar(request, size)


@never_cache
def serve_user_avatar_source(request, user_id, token, suffix):
    fallback_avatar = get_blank_avatar_file(min(settings.MISAGO_AVATARS_SIZES))
    User = get_user_model()

    if user_id > 0:
        try:
            user = User.objects.get(id=user_id)
            if token == store.get_avatar_hash(user, suffix):
                avatar_file = get_user_avatar_file(user.pk, suffix)
            else:
                avatar_file = fallback_avatar
        except User.DoesNotExist:
            avatar_file = fallback_avatar
    else:
        avatar_file = fallback_avatar

    if avatar_file == fallback_avatar:
        avatar_dir = store.get_avatars_dir_path()
    else:
        avatar_dir = store.get_avatars_dir_path(user_id)

    avatar_path = os.path.join(avatar_dir, avatar_file)
    return make_file_response(avatar_path, 'image/png')


def clean_size(size):
    size = int(size)
    if size not in settings.MISAGO_AVATARS_SIZES:
        found_size = max(settings.MISAGO_AVATARS_SIZES)
        for valid_size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
            if valid_size > size:
                found_size = valid_size
        return found_size
    return size


def get_user_avatar_file(user_id, size):
    return '%s_%s.png' % (user_id, size)


def get_blank_avatar_file(size):
    return '%s.png' % size
